"""
This file contains a script to conduct EDA for the annual_data_trim dataset. Follow the instructions
in the code comments to use different graphs etc.

    - Author: Ludwig Scherer
    - Date: 04/16/2025

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load annual dataset
df = pd.read_csv("datasets/annual/annual_data_trim.csv")

# seaborn styling
sns.set_theme(style="whitegrid", context="notebook")

# # ================== dataset overview ==================
# print(df.describe())
# print(df.info())
# print(df.isna().sum())


# # ================== time series visualizations ==================
features = ['absol_temp_c', 'temp_change_c', 'co2_mean', 'co2_growth', 'ch4_mean', 'ch4_growth']
titles = [
    "Temperature Change (C)", 
    "Absolute Temperature (C)", 
    "CO2 Mean (ppm)", 
    "CO2 Growth (ppm/year)", 
    "CH4 Mean (ppm)", 
    "CH4 Growth (ppm/year)"
]

# # comment/uncomment block for sea ice EDA
# features = [
#     'extent_north', 'change_north', 'extent_south', 
#     'change_south', 'extent_global', 'change_global'
# ]
# titles = [
#     "Ice Mass Extent North", 
#     "Ice Mass Change North", 
#     "Ice Mass Extent South", 
#     "Ice Mass Change South", 
#     "Ice Mass Extent Global", 
#     "Ice Mass Change Global"
# ]

# create 3 by 2 grid
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
axes = axes.flatten()

for i, feature in enumerate(features):
    ax = axes[i]

    # plot observed values
    sns.lineplot(data=df, x='year', y=feature, ax=ax, label='Observed')

    # overlay linear trend line
    if df[feature].notna().sum() > 1:
        z = np.polyfit(df['year'], df[feature], 1)
        p = np.poly1d(z)
        ax.plot(df['year'], p(df['year']), color='red', linestyle='--', label='Trend')

    # title and labels
    ax.set_title(titles[i])
    ax.set_xlabel("Year")
    ax.set_ylabel(feature.replace('_', ' ').capitalize())

    ax.legend()

plt.tight_layout()
plt.show()

# # # ================== correlation heat maps ==================
# # split up the features by mean and growth
# mean_features = ['absol_temp_c', 'co2_mean', 'ch4_mean', 'extent_global', 'extent_south', 'extent_north']
# growth_features = ['temp_change_c', 'co2_growth', 'ch4_growth', 'change_north', 'change_south', 'change_global']

# # compute corr matrices
# corr_level = df[mean_features].corr()
# corr_growth = df[growth_features].corr()

# # set up 1 by 2 grid for plots
# fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# # heatmap mean features
# sns.heatmap(corr_level, annot=True, cmap='coolwarm', ax=axes[0], vmin=-1, vmax=1)
# axes[0].set_title("Correlation Matrix: Mean / Average Features")

# # heatmap growth features
# sns.heatmap(corr_growth, annot=True, cmap='coolwarm', ax=axes[1], vmin=-1, vmax=1)
# axes[1].set_title("Correlation Matrix: Growth / Change Features")

# plt.tight_layout()
# plt.show()

# # # ================== pair plots ==================
# # # mean / average features
# # features = ['absol_temp_c', 'co2_mean', 'ch4_mean', 'extent_global', 'extent_south', 'extent_north']

# # growth / change features
# features = [
#     'temp_change_c', 'co2_growth', 'ch4_growth', 'change_north', 'change_south', 'change_global'
# ]

# sns.pairplot(df[features], height=2.5)

# plt.tight_layout()
# plt.show()