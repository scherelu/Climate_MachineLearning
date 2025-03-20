"""
This is the EDA file. After preparing our datasets, we will explore their structure to decide our next steps
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("data/sea_ice.csv", header=0)



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