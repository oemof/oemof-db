#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import pandas as pd
import os.path as path

from . import coastdat
from . import powerplants as pg_pp
from . import tools
from feedinlib import powerplants as pp
from oemof.core.network.entities.components import sources as source


class Feedin:
    ''

    def __init__(self):
        ''
        pass

    def create_fixed_source(self, conn, **kwargs):
        ''
        region = kwargs['region']
        [pv_df, wind_df, cap] = self.get_timeseries(
            conn,
            geometry=region.geom,
            **kwargs)

        if kwargs.get('store', False):
            self.store_full_df(pv_df, wind_df, **kwargs)

        # Summerize the results to one column for pv and one for wind
        df = pd.concat([pv_df.sum(axis=1), wind_df.sum(axis=1)], axis=1)
        feedin_df = df.rename(columns={0: 'pv_pwr', 1: 'wind_pwr'})

        source_list = []

        for stype in feedin_df.keys():
            source_list.append(source.FixedSource(
                uid='_'.join(['DispSrc', region.code, stype]),
                outputs=[obj for obj in region.entities if obj.uid == (
                    'bus', region.name, kwargs['bustype'])],
                val=feedin_df[stype],
                out_max={'_'.join(['b', region.code, 'el']): float(
                    cap.sum()[stype])}))
        return source_list

    def get_timeseries(self, conn, **kwargs):
        ''
        weather = coastdat.get_weather(
            conn, kwargs['geometry'], kwargs['year'])

        pv_df = 0
        pv_cap = {}
        wind_df = 0
        wind_cap = {}

        if not isinstance(weather, list):
            weather = [weather]

        for w_cell in weather:
            ee_pps = pg_pp.get_energymap_pps(
                conn, geometry1=w_cell.geometry, geometry2=kwargs['geometry'])

            # Find type of wind turbine and its parameters according to the
            # windzone.
            wz = tools.get_windzone(conn, w_cell.geometry)

            kwargs['wind_conv_type'] = (kwargs['wka_model_dc'].get(
                wz, kwargs['wka_model']))
            kwargs['d_rotor'] = (kwargs['d_rotor_dc'].get(
                wz, kwargs['d_rotor']))
            kwargs['h_hub'] = (kwargs['h_hub_dc'].get(wz, kwargs['h_hub']))

            # Determine the feedin time series for the weather cell
            # Wind energy
            wind_peak_power = ee_pps[ee_pps.type == 'wind_power'].cap.sum()
            wind_power_plant = pp.WindPowerPlant(**kwargs)
            wind_series = wind_power_plant.feedin(
                weather=w_cell, installed_capacity=wind_peak_power)
            wind_series.name = w_cell.name
            wind_cap[w_cell.name] = wind_peak_power

            # PV
            pv_peak_power = ee_pps[ee_pps.type == 'solar_power'].cap.sum()
            pv_plant = pp.Photovoltaic(**kwargs)
            pv_series = pv_plant.feedin(
                weather=w_cell, peak_power=pv_peak_power)
            pv_series.name = w_cell.name
            pv_cap[w_cell.name] = pv_peak_power

            # Combine the results to a DataFrame
            try:
                pv_df = pd.concat([pv_df, pv_series], axis=1)
                wind_df = pd.concat([wind_df, wind_series], axis=1)
            except:
                pv_df = pv_series.to_frame()
                wind_df = wind_series.to_frame()

        # Write capacity into a dataframe
        capw = pd.Series(pd.DataFrame.from_dict(wind_cap, orient='index')[0])
        capw.name = 'wind_pwr'
        cappv = pd.Series(pd.DataFrame.from_dict(pv_cap, orient='index')[0])
        cappv.name = 'pv_pwr'
        cap = pd.concat([capw, cappv], axis=1)

        return pv_df, wind_df, cap

    def store_full_df(self, pv_df, wind_df, **kwargs):
        ''
        dpath = kwargs.get(
            'dpath', path.join(path.expanduser("~"), '.oemof'))
        filename = kwargs.get('filename', 'feedin_' + kwargs['region'].name)
        fullpath = path.join(dpath, filename)

        if kwargs['store'] == 'hf5':
            pv_df.to_hdf(fullpath + '.hf5', 'pv_pwr')
            wind_df.to_hdf(fullpath + '.hf5', 'wind_pwr')

        if kwargs['store'] == 'csv':
            pv_df.to_csv(fullpath + '_pv.csv')
            wind_df.to_csv(fullpath + '_wind.csv')
