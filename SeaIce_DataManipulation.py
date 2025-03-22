"""
This is the file that was used to manipulate the data in the original sea_ice.csv
"""

import pandas as pd

data = pd.read_csv("data/monthly_ice.csv", header=0)

first_year = data.iloc[0]

data["Change_Global"] = data["Extent_Global"] - first_year["Extent_Global"]
data["Change_North"] = data["Extent_North"] - first_year["Extent_North"]
data["Change_South"] = data["Extent_South"] - first_year["Extent_South"]

# data.to_csv("data/yearly_ice.csv", index=False)

# northern = data[(data["Hemisphere"] == "north")]
# southern = data[(data["Hemisphere"] == "south")]

# north = northern[["Year","Month","Extent"]]
# south = southern[["Year","Month","Extent"]]

# # north.to_csv("north_ice.csv", index=False)
# # south.to_csv("south_ice.csv", index=False)

# north_monthly_ice = north.groupby(["Year","Month"]).agg({"Extent": "mean"}).reset_index()
# south_monthly_ice = south.groupby(["Year","Month"]).agg({"Extent": "mean"}).reset_index()

# north_monthly_ice.to_csv("north_monthly_ice.csv", index=False)
# south_monthly_ice.to_csv("south_monthly_ice.csv", index=False)

# north = pd.read_csv("north_monthly_ice.csv", header=0)
# south = pd.read_csv("south_monthly_ice.csv", header=0)

# global_ice = pd.merge(north, south, on=["Year", "Month"], suffixes= ("_North", "_South"))

# global_ice["Extent_Global"] = global_ice["Extent_North"] + global_ice["Extent_South"]
# data[["Change_Global", "Change_North", "Change_South"]] = data[["Change_Global", "Change_North", "Change_South"]].round(3)
# global_ice.to_csv("global_monthtly_ice.csv", index=False)

# global_ice["Date"] = pd.to_datetime(global_ice[["Year","Month"]].assign(Day=1))

# yearly_ice = global_ice.groupby("Year").agg({ # get the averages per year for each column
#     "Extent_Global": "mean",
#     "Extent_North": "mean",
#     "Extent_South": "mean"
# }).reset_index()