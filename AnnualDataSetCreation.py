"""
This file is used to manipulate all of the datasets containing annual data, and to merge them
into a comprehensive one.

Original Datasets:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change
    co2 annual mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv
    co2 annual growth: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.csv
    ch4 annual mean: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv
    ch4 annual growth: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_gr_gl.csv

NOTE: 

    The missing data between 1961 and 1979 in the co2 annual mean dataset was manually completed
    using https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt 
    
    The missing data betwen 1961 and 1984 in the ch4 annual mean dataset was manually completed
    using https://sealevel.info/co2_and_ch4.html; Since the values are only bi-yearly, interpolation 
    was applied to fill in the values of odd years until 1984.
    
    Thus, the co2_annmean_gl.csv and the ch4_annmean_gl.csv files are not in their original shape 
    anymore in the sense that the missing data is already included. To obtain the original data,
    simply follow the respective link above.
    
    The preprocessed versions of the sea ice and average temperature datasets which are used in this 
    script, can be created by prviously running the scripts in the root folder "PrepareAveTempSet.py" 
    and "PrepareSeaIceSet.py".
    
    For analysis purposes, a trimmed version of the dataset is being created, restricted to the range 
    from 1979 - 2018 That way, the amount of missing data (sea ice data) is reduced drastically.

"""

import pandas as pd

temp_change_set = pd.read_csv("data/preprocessed/annual_clean.csv", header=0)
ch4_mean = pd.read_csv("data/preprocessed/ch4_annmean_gl.csv", header=0)
ch4_growth = pd.read_csv("data/original/NOAA/ch4_gr_gl.csv", header=45)
co2_mean = pd.read_csv("data/preprocessed/co2_annmean_gl.csv", header=0)
co2_growth = pd.read_csv("data/original/NOAA/co2_gr_gl.csv", header=43)
sea_ice = pd.read_csv("data/preprocessed/ice_annual.csv", header=0)


ch4_growth = ch4_growth[['year', 'ann inc']]
ch4_combo = pd.merge(ch4_mean, ch4_growth, on='year', how='left')
ch4_combo.rename(columns={'ann inc': 'ch4_growth'}, inplace=True)
mask = (ch4_combo['year'] >= 1960) & (ch4_combo['year'] <= 1984)
ch4_combo.loc[mask & ch4_combo['ch4_growth'].isna(), 'ch4_growth'] = round(
    ch4_combo.loc[mask, "ch4_mean"].diff().shift(-1), 4
)

# convert ch4 values from ppb to ppm
ch4_combo[['ch4_mean', 'ch4_growth']] = round(ch4_combo[['ch4_mean', 'ch4_growth']] / 1000, 4)

mask = (ch4_combo['year'] >= 1961) & (ch4_combo['year'] <= 2020) # reduce data to 1961 - 2020
ch4_combo = ch4_combo[mask]

co2_growth = co2_growth[['year', 'ann inc']]
co2_growth.rename(columns={'ann inc': 'co2_growth'}, inplace=True)
co2_combo = pd.merge(co2_mean, co2_growth, on='year', how='left')
mask = (co2_combo['year'] >= 1961) & (co2_combo['year'] <= 2020) # reduce data to 1961 - 2020
co2_combo = co2_combo[mask]

co2_ch4_combo = pd.merge(co2_combo, ch4_combo, on='year', how='left')

sea_ice.rename(columns={'Year' : 'year'}, inplace=True)
co2_ch4_ice_combo = pd.merge(co2_ch4_combo, sea_ice, on='year', how='left')

temp_change_set['absol_temp_c'] = round(temp_change_set['temp_change_c'] + 14, 4)

annual_data = pd.merge(temp_change_set, co2_ch4_ice_combo, on='year', how='left')

mask = ((annual_data['year'] >= 1979) & (annual_data['year'] <= 2018))
annual_data_trim = annual_data[mask]

annual_data.to_csv("data/annual/annual_data.csv", index=False)
annual_data_trim.to_csv("data/annual/annual_data_trim.csv", index=False)