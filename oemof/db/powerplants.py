# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 11:08:15 2015

This is a collection of helper functions which work on there own an can be
used by various classes. If there are too many helper-functions, they will
be sorted in different modules.

All special import should be in try/except loops to avoid import errors.
"""

import logging
import pandas as pd

de_en = {
    'Braunkohle': 'lignite',
    'Steinkohle': 'hard_coal',
    'Erdgas': 'natural_gas',
    'Öl': 'oil',
    'Solarstrom': 'solar_power',
    'Windkraft': 'wind_power',
    'Biomasse': 'biomass',
    'Wasserkraft': 'hydro_power',
    'Gas': 'methan',
    'Mineralölprodukte': 'mineral_oil',
    'Abfall': 'waste',
    'Sonstige Energieträger\n(nicht erneuerbar) ': 'waste',
    'Pumpspeicher': 'pumped_storage'}

translator = lambda x: de_en[x]


def get_all_power_plants(conn, geometry):
    return (pd.concat([get_bnetza_pps(conn, geometry),
                       get_energymap_pps(conn, geometry)],
                      ignore_index=True))


def get_energymap_pps(conn, geometry1, geometry2=None, tsum=True):
    # TODO@Günni
    sql = """
        SELECT anlagentyp, anuntertyp, p_nenn_kwp
        FROM oemof_test.energy_map as ee
        WHERE st_contains(ST_GeomFromText('{wkt}',4326), ee.geom)
        """.format(wkt=geometry1.wkt)

    if geometry2 is None:
        sql += ';'
    else:
        sql += '''AND st_contains(ST_GeomFromText('{wkt}',4326),
            ee.geom);'''.format(wkt=geometry2.wkt)
    df_full = pd.DataFrame(
        conn.execute(sql).fetchall(), columns=['type', 'subtype', 'cap'])
    df = pd.DataFrame(columns=['type', 'cap'])
    if tsum:
        typelist = df_full.type.unique()
        for i in range(len(typelist)):
            cap_sum = df_full[df_full.type == typelist[i]].cap.sum()
            df.loc[i] = [typelist[i], cap_sum]
    else:
        df = df_full
    df['type'] = df['type'].apply(translator)
    return df


def get_bnetza_pps(conn, geometry):
    # TODO@Günni
    sql = """
        SELECT auswertung, ersatzbrennstoff, el_nennleistung
        FROM oemof_test.geo_power_plant_bnetza_2014 as pp
        WHERE st_contains(
        ST_GeomFromText('{wkt}',4326), ST_Transform(pp.geom, 4326))
        """.format(wkt=geometry.wkt)
    df = pd.DataFrame(
        conn.execute(sql).fetchall(), columns=['type', 'subtype', 'cap'])
    df['type'] = df['type'].apply(translator)
    return df
