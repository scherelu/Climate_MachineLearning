"""
This is the EDA file. After preparing our datasets, we will explore their structure to decide our next steps
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr

data = xr.open_dataset("NOAA_GlobalTemp.nc")
dataframe = data.to_dataframe()

dataframe.to_csv("NOAA_Global_Temp.csv", index=False)

# monthly = pd.read_csv("data/monthly_ice.csv", header=0)
# yearly = pd.read_csv("data/yearly_ice.csv", header=0)

# monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(Day=1))
# yearly["Year"] = pd.to_datetime(yearly["Year"], format="%Y")

# plt.figure(figsize=(12,6))

# plt.plot(yearly["Year"], yearly["Change_Global"], label="Yearly_Global", color="black", linewidth=2)
# plt.plot(yearly["Year"], yearly["Change_North"], label="Yearly_North", color="blue", linewidth=2)
# plt.plot(yearly["Year"], yearly["Change_South"], label="Yearly_South", color="red", linewidth=2)

# plt.xlabel("Year")
# plt.ylabel("Seas ice area in Million km^2")
# plt.title("Yearly Change of Sea Ice Extent, relative to 1979 (1979-2018)")
# plt.legend()
# plt.grid(True)

# plt.show()

# feature_names = data.columns
# shape = data.shape
# rows = shape[0]
# columns = shape[1]

# print(f"shape of the dataset (rows, columns): {shape}")
# print(f"feature names: {feature_names}")

# columns_to_plot = ['Date','Continent', 'Temperature', 'CO2 Emissions', 'Humidity', 'Precipitation']

# sns.pairplot(data[columns_to_plot], height = 3)
# plt.tight_layout()
# plt.show()