"""
This file is used to manipulate all of our datasets and to merge them into a comprehenseive one.
The annual data set is already merged, the monthly dataset is still work in progress. Sadly I realized too late
that we need to hand this in aswell. While I do have a record of how I manipulated the datafiles, I did not have
time to reconstruct all of the python code that went into it. The methods how we attained our final datasets
will of course be included in our final report for transparency.
"""

import pandas as pd
import numpy as np


data = pd.read_csv("data/annual/annual_data.csv", header=0)

print(data.shape)

# data1 = pd.read_csv("data/annual/co2_ch4_ice_combo.csv", header=0)

# combo = pd.merge(data, data1, on="Year", how="left")

# combo.to_csv("data/annual/annual_data.csv", index=False)

# months = ["January", "February", "March", "April", "May", "June", "July", "August",
#           "September", "October", "November", "December"]

# seasons = ["Dec?Jan?Feb","Mar?Apr?May","Jun?Jul?Aug", "Sep?Oct?Nov"]

# data = data[["year","ann inc"]]

# data.to_csv("data/annual/co2_gr_gl.csv", index=False)

# data["Temp_Change_C"] = data["Value"]

## --------------------------------------------------------------------------
### This block was to remove countries that were missing entry years, such as Yugoslavia, USSR, Sudan, etc.
# # croup by country and check completeness
# incomplete_countries = []

# expected_years = set(range(1961,2021))

# for country, group in data.groupby("Country"):
#     years_present = set(group["Year"])
#     if years_present != expected_years:
#         missing_years = sorted(expected_years - years_present)
#         incomplete_countries.append((country, len(missing_years), missing_years))

# # create a DataFrame of incomplete countries
# incomplete_df = pd.DataFrame(incomplete_countries, columns=["Country", "Missing_Count", "Missing_Years"])

# complete_countries = set(data["Country"].unique()) - set(incomplete_df["Country"])
# clean_data = data[data["Country"].isin(complete_countries)]

# clean_data.to_csv("cleaned_annual_temp.csv", index=False)
