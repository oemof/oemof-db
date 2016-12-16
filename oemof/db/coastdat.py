#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import pandas as pd
import numpy as np
from pytz import timezone
from datetime import datetime
import feedinlib.weather as weather
from . import tools
from shapely.wkt import loads as wkt_loads


def get_weather(conn, geometry, year):
    r"""
    Get the weather data for the given geometry and create an oemof
    weather object.
    """
    rename_dc = {
        'ASWDIFD_S': 'dhi',
        'ASWDIR_S': 'dirhi',
        'PS': 'pressure',
        'T_2M': 'temp_air',
        'WSS_10M': 'v_wind',
        'Z0': 'z0'}

    if geometry.geom_type in ['Polygon', 'MultiPolygon']:
        # Create MultiWeather
        # If polygon covers only one data set switch to SingleWeather
        sql_part = """
            SELECT sp.gid, ST_AsText(point.geom), ST_AsText(sp.geom)
            FROM coastdat.cosmoclmgrid AS sp
            JOIN coastdat.spatial AS point ON (sp.gid=point.gid)
            WHERE st_intersects(ST_GeomFromText('{wkt}',4326), sp.geom)
            """.format(wkt=geometry.wkt)
        df = fetch_raw_data(sql_weather_string(year, sql_part), conn, geometry)
        obj = create_multi_weather(df, rename_dc)
    elif geometry.geom_type == 'Point':
        # Create SingleWeather
        sql_part = """
            SELECT sp.gid, ST_AsText(point.geom), ST_AsText(sp.geom)
            FROM coastdat.cosmoclmgrid AS sp
            JOIN coastdat.spatial AS point ON (sp.gid=point.gid)
            WHERE st_contains(sp.geom, ST_GeomFromText('{wkt}',4326))
            """.format(wkt=geometry.wkt)
        df = fetch_raw_data(sql_weather_string(year, sql_part), conn, geometry)
        obj = create_single_weather(df, rename_dc)
    else:
        logging.error('Unknown geometry type: {0}'.format(geometry.geom_type))
        obj = None
    return obj


def sql_weather_string(year, sql_part):
    """
    Creates an sql-string to read all datasets within a given geometry.
    """
    # TODO@Günni. Replace sql-String with alchemy/GeoAlchemy
    # Create string parts for where conditions

    return '''
    SELECT tsptyti.*, y.leap
    FROM coastdat.year as y
    INNER JOIN (
        SELECT tsptyd.*, sc.time_id
        FROM coastdat.scheduled as sc
        INNER JOIN (
            SELECT tspty.*, dt.name, dt.height
            FROM coastdat.datatype as dt
            INNER JOIN (
                SELECT tsp.*, typ.type_id
                FROM coastdat.typified as typ
                INNER JOIN (
                    SELECT spl.*, t.tsarray, t.id
                    FROM coastdat.timeseries as t
                    INNER JOIN (
                        SELECT sps.*, l.data_id
                        FROM (
                            {sql_part}
                            ) as sps
                        INNER JOIN coastdat.located as l
                        ON (sps.gid = l.spatial_id)) as spl
                    ON (spl.data_id = t.id)) as tsp
                ON (tsp.id = typ.data_id)) as tspty
            ON (tspty.type_id = dt.id)) as tsptyd
        ON (tsptyd.id = sc.data_id))as tsptyti
    ON (tsptyti.time_id = y.year)
    where y.year = '{year}'
    ;'''.format(year=year, sql_part=sql_part)


def fetch_raw_data(sql, connection, geometry):
    """
    Fetch the coastdat2 from the database, adapt it to the local time zone
    and create a time index.
    """
    tmp_dc = {}
    weather_df = pd.DataFrame(
        connection.execute(sql).fetchall(), columns=[
            'gid', 'geom_point', 'geom_polygon', 'data_id', 'time_series',
            'dat_id', 'type_id', 'type', 'height', 'year', 'leap_year']).drop(
        'dat_id', 1)

    # Get the timezone of the geometry
    tz = tools.tz_from_geom(connection, geometry)

    for ix in weather_df.index:
        # Convert the point of the weather location to a shapely object
        weather_df.loc[ix, 'geom_point'] = wkt_loads(
            weather_df['geom_point'][ix])

        # Roll the dataset forward according to the timezone, because the
        # dataset is based on utc (Berlin +1, Kiev +2, London +0)
        utc = timezone('utc')
        offset = int(utc.localize(datetime(2002, 1, 1)).astimezone(
            timezone(tz)).strftime("%z")[:-2])

        # Get the year and the length of the data array
        db_year = weather_df.loc[ix, 'year']
        db_len = len(weather_df['time_series'][ix])

        # Set absolute time index for the data sets to avoid errors.
        tmp_dc[ix] = pd.Series(
            np.roll(np.array(weather_df['time_series'][ix]), offset),
            index=pd.date_range(pd.datetime(db_year, 1, 1, 0),
                                periods=db_len, freq='H', tz=tz))
    weather_df['time_series'] = pd.Series(tmp_dc)
    return weather_df


def create_single_weather(df, rename_dc):
    """Create an oemof weather object for the given geometry"""
    my_weather = weather.FeedinWeather()
    data_height = {}
    name = None
    # Create a pandas.DataFrame with the time series of the weather data set
    weather_df = pd.DataFrame(index=df.time_series.iloc[0].index)
    for row in df.iterrows():
        key = rename_dc[row[1].type]
        weather_df[key] = row[1].time_series
        data_height[key] = row[1].height if not np.isnan(row[1].height) else 0
        name = row[1].gid
    my_weather.data = weather_df
    my_weather.timezone = weather_df.index.tz
    my_weather.longitude = df.geom_point.iloc[0].x
    my_weather.latitude = df.geom_point.iloc[0].y
    my_weather.geometry = df.geom_point.iloc[0]
    my_weather.data_height = data_height
    my_weather.name = name
    return my_weather


def create_multi_weather(df, rename_dc):
    """Create a list of oemof weather objects if the given geometry is a polygon
    """
    weather_list = []
    # Create a pandas.DataFrame with the time series of the weather data set
    # for each data set and append them to a list.
    for gid in df.gid.unique():
        gid_df = df[df.gid == gid]
        obj = create_single_weather(gid_df, rename_dc)
        weather_list.append(obj)
    return weather_list
