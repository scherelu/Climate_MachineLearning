"""
This file is used to prepare and split the large amount of data contained in the sea_ice.csv
file. For example, the data of northern and southern hemisphere is being merged, incomplete years at the
beginning and end of the set are discarded, and new features, namely the change in relation to the first
month on record are created for both the Northern and Southern hemisphere, as well as globally. Then, the
mean values of each feature for every year is computed, and the resulting data extracted into an annual
dataset.

Original Dataset:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data

"""

import pandas as pd

data = pd.read_csv("data/original/sea_ice.csv", header=0)

# discard unnecessary columns
columns_to_keep = ['Year', 'Month', 'Day', 'Extent', 'Hemisphere']
data = data[columns_to_keep]

# split data in to northern and southern hemisphere data
northern = data[(data["Hemisphere"] == "north")]
southern = data[(data["Hemisphere"] == "south")]

# group by year and month, then compute the mean extent
northern = round(northern.groupby(["Year", "Month"], as_index=False)["Extent"].mean(),3)
southern = round(southern.groupby(["Year", "Month"], as_index=False)["Extent"].mean(), 3)

# remove rows where year is 1978 or 2019 (data incomplete for those years and no values beyond / before)
northern = northern[(northern["Year"] != 1978) & (northern["Year"] != 2019)]
southern = southern[(southern["Year"] != 1978) & (southern["Year"] != 2019)]

# rename columns for mergings
northern.rename(columns={'Extent': 'Extent_North'}, inplace=True)
southern.rename(columns={'Extent': 'Extent_South'}, inplace=True)

# merge on year and month
combined_hem = pd.merge(northern, southern, on=["Year", "Month"], how="inner")
combined_hem["Extent_Global"] = round(combined_hem["Extent_North"] + combined_hem["Extent_South"], 3)

# compute first extent value in the dataset for each month
north_first = combined_hem.groupby("Month")["Extent_North"].transform("first")
south_first = combined_hem.groupby("Month")["Extent_South"].transform("first")

# calculate the monthly change relative to the value of the first respective month 
combined_hem["Change_North"] = round(combined_hem["Extent_North"] - north_first, 3)
combined_hem["Change_South"] = round(combined_hem["Extent_South"] - south_first, 3)

# get the combined global change
combined_hem["Change_Global"] = round(combined_hem["Change_North"] + combined_hem["Change_South"], 3)

# create annual data by grouping by year and computing the mean value of all given columns within that group
annual_data = round(combined_hem.groupby(["Year"], as_index=False)[[
    "Extent_North", "Extent_South", "Extent_Global", 
    "Change_North", "Change_South","Change_Global"
]].mean(), 3)

combined_hem.rename(columns={'Month': 'Month_Num'}, inplace=True)

# map to convert numerical month values to categorical 
month_name_map = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

# map the numerical month values to categorical
combined_hem["Month"] = combined_hem["Month_Num"].map(month_name_map)

# impose order on the months categorical column
month_order = list(month_name_map.values())
combined_hem["Month"] = pd.Categorical(
    combined_hem["Month"],
    categories=month_order,
    ordered=True
)

# impose order on the months column
month_order = list(month_name_map.keys())
combined_hem["Month_Num"] = pd.Categorical(
    combined_hem["Month_Num"],
    categories=month_order,
    ordered=True
)

# store data
annual_data.to_csv('data/temp/ice_annual.csv', index=False)
combined_hem.to_csv('data/temp/ice_monthly.csv', index=False)