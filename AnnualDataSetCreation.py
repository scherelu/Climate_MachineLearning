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

"""

import pandas as pd

temp_change_set = pd.read_csv("data/temp/annual_clean.csv", header=0)
ch4_mean = pd.read_csv("data/original/NOAA/ch4_annmean_gl.csv", header=43)
ch4_growth = pd.read_csv("data/original/NOAA/ch4_gr_gl.csv", header=45)
co2_mean = pd.read_csv("data/original/NOAA/co2_annmean_gl.csv", header=37)
co2_growth = pd.read_csv("data/original/NOAA/co2_gr_gl.csv", header=42)
sea_ice = pd.read_csv("data/temp/ice_annual.csv", header=0)