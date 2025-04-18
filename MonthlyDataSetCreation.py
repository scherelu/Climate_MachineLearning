"""
This file is used to manipulate all of our monthly datasets and to merge them into a comprehensive one.

Original Datasets:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change
    co2 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv
    ch4 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv

NOTE: 
    The missing data between 1961 and 1979 in the co2 annual mean dataset was manually completed using  
    https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt 
    
    The missing data betwen 1961 and 1984 in the ch4 annual mean dataset was manually completed using
    https://sealevel.info/co2_and_ch4.html ; Since the recorded values are only biyearly, interpolation 
    was used.
    
    For analysis purposes, a trimmed version is being created, restricted to the range from 1979 - 2018
    That way, the amount of missing data is reduced drastically.

"""

import pandas as pd

temp_set_month = pd.read_csv('data/preprocessed/monthly_clean.csv', header=0)
ice_month = pd.read_csv('data/preprocessed/ice_monthly.csv', header=0)
co2_mean = pd.read_csv('data/original/NOAA/co2_mm_gl.csv', header=38)
ch4_mean = pd.read_csv('data/original/NOAA/ch4_mm_gl.csv', header=45)

columns_to_keep = ['year', 'month', 'average', 'trend']

co2_mean = co2_mean[columns_to_keep]
ch4_mean = ch4_mean[columns_to_keep]

mask = (co2_mean['year'] <= 2021) # remove unwanted years
co2_mean = co2_mean[mask]

mask = (ch4_mean['year'] > 1983) & (ch4_mean['year'] <= 2021) # remove unwanted years (1983 incomplete)
ch4_mean[mask]

co2_mean = co2_mean.sort_values(['month', 'year'])
ch4_mean = ch4_mean.sort_values(['month', 'year'])

co2_mean['co2_growth'] = (
    co2_mean.loc[(co2_mean['year'] >= 1979) & (co2_mean['year'] <= 2021)]
    .groupby('month')['average']
    .diff()
    .shift(-1)
    .round(4)
)

ch4_mean['ch4_growth'] = (
    ch4_mean.loc[(ch4_mean['year'] >= 1983) & (ch4_mean['year'] <= 2021)]
    .groupby('month')['average']
    .diff()
    .shift(-1)
    .round(4)
)

# convert ch4 values from ppb to ppm
ch4_mean[['average', 'trend','ch4_growth']] = round(ch4_mean[['average', 'trend','ch4_growth']] / 1000, 4)

ch4_mean.rename(columns={'average': 'ch4_average', 'trend': 'ch4_trend'}, inplace=True)
co2_mean.rename(columns={'average': 'co2_average', 'trend': 'c02_trend'}, inplace=True)

co2_ch4_combo = pd.merge(co2_mean, ch4_mean, on=['year', 'month'], how='left')

mask = (co2_ch4_combo['year'] <= 2020)
co2_ch4_combo = co2_ch4_combo[mask]

co2_ch4_ice_combo = pd.merge(co2_ch4_combo, ice_month, on=['year', 'month'], how='left')
co2_ch4_ice_combo = co2_ch4_ice_combo.sort_values(['month', 'year'])

monthly_data = pd.merge(temp_set_month, co2_ch4_ice_combo, on=['year', 'month', 'month_cat'], how='left')
monthly_data['decimal_date'] = round(monthly_data['year'] + (monthly_data['month'] - 1) / 12.0, 4)


column_order = [
    'country', 'year', 'month_cat', 'month', 'decimal_date', 'temp_change_c', 'co2_average', 'c02_trend',
    'co2_growth', 'ch4_average', 'ch4_trend', 'ch4_growth', 'extent_north', 'extent_south',
    'extent_global', 'change_north', 'change_south', 'change_global'
]

monthly_data = monthly_data[column_order]

mask = ((monthly_data['year'] >= 1979) & (monthly_data['year'] <= 2018))
monthly_data_trim = monthly_data[mask]

monthly_data.to_csv("data/monthly/monthly_data.csv", index=False)
monthly_data_trim.to_csv("data/monthly/monthly_data_trim.csv", index=False)