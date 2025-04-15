"""
This file is used to manipulate all of our datasets and to merge them into a comprehenseive one.
The annual data set is already merged, the monthly dataset is still work in progress. Sadly I realized too late
that we need to hand this in aswell. While I do have a record of how I manipulated the datafiles, I did not have
time to reconstruct all of the python code that went into it. The methods how we attained our final datasets
will of course be included in our final report for transparency.

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
    .round(2)
)

ch4_mean['ch4_growth'] = (
    ch4_mean.loc[(ch4_mean['year'] >= 1983) & (ch4_mean['year'] <= 2021)]
    .groupby('month')['average']
    .diff()
    .shift(-1)
    .round(2)
)

ch4_mean[['average', 'trend','ch4_growth']] = round(ch4_mean[['average', 'trend','ch4_growth']] / 10, 2)

co2_ch4_combo = pd.merge(co2_mean, ch4_mean, on=['year', 'month'], how='left')

mask = (co2_ch4_combo['year'] <= 2020)
co2_ch4_combo = co2_ch4_combo[mask]

co2_ch4_ice_combo = pd.merge(co2_ch4_combo, ice_month, on=['year', 'month'], how='left')
co2_ch4_ice_combo = co2_ch4_ice_combo.sort_values(['month', 'year'])

monthly_data = pd.merge(temp_set_month, co2_ch4_ice_combo, on=['year', 'month'], how='left')

monthly_data.to_csv("data/monthly/monthly_data.csv", index=False)