"""
This is the file that was used to manipulate the data in the original sea_ice.csv, and write the new dataset
to the global_monthly_ice.csv
"""

import pandas as pd

# data = pd.read_csv("data/sea_ice.csv", header=0)

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

north = pd.read_csv("north_monthly_ice.csv", header=0)
south = pd.read_csv("south_monthly_ice.csv", header=0)

global_ice = pd.merge(north, south, on=["Year", "Month"], suffixes= ("_North", "_South"))

global_ice["Extent_Global"] = global_ice["Extent_North"] + global_ice["Extent_South"]
global_ice[["Extent_Global", "Extent_North", "Extent_South"]] = global_ice[["Extent_Global", "Extent_North", "Extent_South"]].round(3)

global_ice.to_csv("global_monthtly_ice.csv", index=False)