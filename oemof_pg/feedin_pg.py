#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

def fetch_ee_feedin(self, conn, **site):
    site['connection'] = conn
    pv_df = 0
    wind_df = 0
    if self.power_plants.get('re', None) is None:
        self.power_plants['re'] = (
            pp.Power_Plants().get_empty_power_plant_df())

    # Define height dict
    data_height = {}
    for key in self.weather.datatypes:
        name = self.weather.name_dc[key]
        data_height[name] = self.weather.get_data_heigth(name)
        if data_height[name] is None:
            data_height[name] = 0

    laenge = len(self.weather.gid)

    for gid in self.weather.gid:
        logging.debug(laenge)
        # Get the geometry for the given weather raster field
        tmp_geom = self.weather.get_geometry_from_gid(gid)

        # Get all Power Plants for raster field
        ee_pp = pp.Power_Plants().get_all_re_power_plants(
            conn, tmp_geom, self.geometry)

        # Add the powerplants to the power plant table of the region
        self.power_plants['re'] = pd.concat(
            [ee_pp, self.power_plants['re']], ignore_index=True)

        # Find type of wind turbine and its parameters according to the
        # windzone.
        wz = pg_helpers.get_windzone(conn, tmp_geom)
        site['wind_conv_type'] = (site['wka_model_dc'].get(
            wz, site['wka_model']))
        site['d_rotor'] = (site['d_rotor_dc'].get(wz, site['d_rotor']))
        site['h_hub'] = (site['h_hub_dc'].get(wz, site['h_hub']))

        # Define weather object of the feedinlib
        self.weather.set_feedin_dataset(gid)

        # Determine the feedin time series for the weather field
        # Wind energy
        wind_peak_power = ee_pp[ee_pp.type == 'Windkraft'].p_kw_peak.sum()
        wind_power_plant = plants.WindPowerPlant(**site)
        wind_series = wind_power_plant.feedin(
            weather=self.weather,
            installed_capacity=wind_peak_power)
        wind_series.name = gid

        # PV
        pv_peak_power = ee_pp[ee_pp.type == 'Solarstrom'].p_kw_peak.sum()
        pv_plant = plants.Photovoltaic(**site)
        pv_series = pv_plant.feedin(
            weather=self.weather, peak_power=pv_peak_power)
        pv_series.name = gid

        # Combine the results to a DataFrame
        try:
            pv_df = pd.concat([pv_df, pv_series], axis=1)
            wind_df = pd.concat([wind_df, wind_series], axis=1)
        except:
            pv_df = pv_series.to_frame()
            wind_df = wind_series.to_frame()

        laenge -= 1

    if site.get('store'):
        dpath = site.get(
            'dpath', path.join(path.expanduser("~"), '.oemof'))
        filename = site.get('filename', self.name)
        fullpath = path.join(dpath, filename)

        if site['store'] == 'hf5':
            pv_df.to_hdf(fullpath + '.hf5', 'pv_pwr')
            wind_df.to_hdf(fullpath + '.hf5', 'wind_pwr')

        if site['store'] == 'csv':
            pv_df.to_csv(fullpath + '_pv.csv')
            wind_df.to_csv(fullpath + '_wind.csv')

    # Summerize the results to one column for pv and one for wind
    df = pd.concat([pv_df.sum(axis=1), wind_df.sum(axis=1)], axis=1)
    self.feedin = df.rename(columns={0: 'pv_pwr', 1: 'wind_pwr'})
    return self
