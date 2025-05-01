"""
This file is used to prepare and split the large amount of data contained in the ice_north/S_01_extent_v3.0.csv
file. For example, the data of northern and southern hemisphere is being merged, incomplete years at the
beginning and end of the set are discarded, and new features, namely the change in relation to the first
month on record are created for both the Northern and Southern hemisphere, as well as globally. Then, the
mean values of each feature for every year is computed, and the resulting data extracted into an annual
dataset.

Original Datasets:

    All datasets can be obtained from: https://noaadata.apps.nsidc.org/NOAA/G02135/ 

    - Author: Ludwig Scherer
    - Date: 05/01/2025

"""

import pandas as pd
import numpy as np

# Northern data
N_Jan = pd.read_csv("data/original/ice_north/N_01_extent_v3.0.csv", header=0)
N_Feb = pd.read_csv("data/original/ice_north/N_02_extent_v3.0.csv", header=0)
N_Mar = pd.read_csv("data/original/ice_north/N_03_extent_v3.0.csv", header=0)
N_Apr = pd.read_csv("data/original/ice_north/N_04_extent_v3.0.csv", header=0)
N_May = pd.read_csv("data/original/ice_north/N_05_extent_v3.0.csv", header=0)
N_Jun = pd.read_csv("data/original/ice_north/N_06_extent_v3.0.csv", header=0)
N_Jul = pd.read_csv("data/original/ice_north/N_07_extent_v3.0.csv", header=0)
N_Aug = pd.read_csv("data/original/ice_north/N_08_extent_v3.0.csv", header=0)
N_Sep = pd.read_csv("data/original/ice_north/N_09_extent_v3.0.csv", header=0)
N_Oct = pd.read_csv("data/original/ice_north/N_10_extent_v3.0.csv", header=0)
N_Nov = pd.read_csv("data/original/ice_north/N_11_extent_v3.0.csv", header=0)
N_Dec = pd.read_csv("data/original/ice_north/N_12_extent_v3.0.csv", header=0)

# Southern data
S_Jan = pd.read_csv("data/original/ice_south/S_01_extent_v3.0.csv", header=0)
S_Feb = pd.read_csv("data/original/ice_south/S_02_extent_v3.0.csv", header=0)
S_Mar = pd.read_csv("data/original/ice_south/S_03_extent_v3.0.csv", header=0)
S_Apr = pd.read_csv("data/original/ice_south/S_04_extent_v3.0.csv", header=0)
S_May = pd.read_csv("data/original/ice_south/S_05_extent_v3.0.csv", header=0)
S_Jun = pd.read_csv("data/original/ice_south/S_06_extent_v3.0.csv", header=0)
S_Jul = pd.read_csv("data/original/ice_south/S_07_extent_v3.0.csv", header=0)
S_Aug = pd.read_csv("data/original/ice_south/S_08_extent_v3.0.csv", header=0)
S_Sep = pd.read_csv("data/original/ice_south/S_09_extent_v3.0.csv", header=0)
S_Oct = pd.read_csv("data/original/ice_south/S_10_extent_v3.0.csv", header=0)
S_Nov = pd.read_csv("data/original/ice_south/S_11_extent_v3.0.csv", header=0)
S_Dec = pd.read_csv("data/original/ice_south/S_12_extent_v3.0.csv", header=0)

north_data = pd.concat([N_Jan, N_Feb, N_Mar, N_Apr, N_May, N_Jun, N_Jul, N_Aug, N_Sep, N_Oct, N_Nov, N_Dec])
south_data = pd.concat([S_Jan, S_Feb, S_Mar, S_Apr, S_May, S_Jun, S_Jul, S_Aug, S_Sep, S_Oct, S_Nov, S_Dec])

north_data.columns = north_data.columns.str.strip()
south_data.columns = south_data.columns.str.strip()

columns_to_keep = ['year', 'mo', 'extent', 'area']

north_data = north_data[columns_to_keep]
south_data = south_data[columns_to_keep]

north_data.rename(columns={'mo': 'month', 'extent' : 'extent_north', 'area': 'area_north'}, inplace=True)
south_data.rename(columns={'mo': 'month', 'extent' : 'extent_south', 'area': 'area_south'}, inplace=True)

# remove rows where year is less than 1978 or greater 2020 (for compatibility with other datasets)
north_data = north_data[(north_data["year"] >= 1978) & (north_data["year"] <= 2020)]
south_data = south_data[(south_data["year"] >= 1978) & (south_data["year"] <= 2020)]

combined = pd.merge(north_data, south_data, on=["year", "month"], how="inner")

combined = combined.mask(combined < 0, np.nan)
combined = combined.interpolate(method='linear')

# calculate global stats
combined["extent_global"] = combined["extent_north"] + combined["extent_south"]
combined["area_global"] = combined["area_north"] + combined["area_south"]

# compute first extent value in the dataset for each month
north_first = combined.groupby("month")["extent_north"].transform("first")
south_first = combined.groupby("month")["extent_south"].transform("first")

# calculate the monthly extent change relative to the value of the first respective month 
combined["extent_change_north"] = combined["extent_north"] - north_first
combined["extent_change_south"] = combined["extent_south"] - south_first

# same for the area
north_first = combined.groupby("month")["area_north"].transform("first")
south_first = combined.groupby("month")["area_south"].transform("first")

combined["area_change_north"] = combined["extent_north"] - north_first
combined["area_change_south"] = combined["extent_south"] - south_first

# get the combined global change
combined["extent_change_global"] = combined["extent_change_north"] + combined["extent_change_south"]
combined["area_change_global"] = combined["area_change_north"] + combined["area_change_south"]

# create annual data by grouping by year and computing the mean value of all given columns within that group
annual_data = combined.groupby(["year"], as_index=False)[[
    "extent_north", "extent_south", "extent_global", "area_north", "area_south", "area_global",
    "extent_change_north", "extent_change_south","extent_change_global", 
    "area_change_north", "area_change_south", "area_change_global"
]].mean()

annual_data = annual_data[(annual_data["year"] >= 1979)]

combined = combined.round(3)
annual_data = annual_data.round(3)

# map to convert numerical month values to categorical 
month_name_map = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

# map the numerical month values to categorical
combined["month_cat"] = combined["month"].map(month_name_map)

# store data
annual_data.to_csv('data/preprocessed/ice_annual.csv', index=False)
combined.to_csv('data/preprocessed/ice_monthly.csv', index=False)