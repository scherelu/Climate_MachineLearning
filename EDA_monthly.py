import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load monthly dataset
df = pd.read_csv("data/monthly/monthly_data_trim.csv")

# seaborn styling
sns.set_theme(style="whitegrid", context="notebook")

# # ================== dataset overview ==================
# print(df.describe())
# print(df.info())
# print(df.isna().sum())

# # ================== time series visualizations ==================
# # NOTE: Rows are sorted by month, year, country
# # You may want to subset by country if comparing over time

# # Example: Filter for a single country (optional)
# # df = df[df['country'] == 'Germany']

# # # greenhouse features
# # features = ['co2_average', 'co2_growth', 'ch4_average', 'ch4_growth', 'temp_change_c']
# # titles = [
# #     "CO2 Average (ppm)",
# #     "CO2 Growth (ppm/month)",
# #     "CH4 Average (ppm)",
# #     "CH4 Growth (ppm/month)",
# #     "Temperature Change (C)"
# # ]

# # # growth / change features
# features = [ 'extent_north', 'change_north', 'extent_south', 'change_south', 'extent_global', 'change_global']
# titles = [
#     "Sea Ice Extent North",
#     "Ice Mass Change North",
#     "Sea Ice Extent South",
#     "Ice Mass Change South",
#     "Sea Ice Extent Global",
#     "Ice Mass Change Global"
# ]

# # create 3 by 2 grid
# fig, axes = plt.subplots(3, 2, figsize=(14, 12))
# axes = axes.flatten()
# # axes[5].axis('off') # uncomment this line, when graphing the greenhouse data (only 5 features) 
 
# for i, feature in enumerate(features):
#     ax = axes[i]

#     # plot values by decimal date for continuous x-axis
#     sns.lineplot(data=df, x='decimal_date', y=feature, ax=ax, label='Observed')

#     # linear trend line
#     valid = df[feature].notna() # filter out nan values
#     if valid.sum() > 1:
#         z = np.polyfit(df.loc[valid, 'decimal_date'], df.loc[valid, feature], 1)
#         p = np.poly1d(z)
#         ax.plot(df['decimal_date'], p(df['decimal_date']), color='red', linestyle='--', label='Trend')


#     ax.set_title(titles[i])
#     ax.set_xlabel("Year")
#     ax.set_ylabel(feature.replace('_', ' ').capitalize())
#     ax.legend()

# plt.tight_layout()
# plt.show()

# # ================== correlation heat maps ==================
# # mean / average features
# mean_features = ['co2_average', 'ch4_average', 'extent_global', 'extent_north', 'extent_south']

# # growth / change features
# growth_features = ['co2_growth', 'ch4_growth', 'temp_change_c', 'change_north', 'change_south', 'change_global']

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

# # ================== pair plots ==================
# # mean / average features
# features = ['co2_average', 'ch4_average', 'extent_global', 'extent_north', 'extent_south']

# growth / change features
features = ['co2_growth', 'ch4_growth', 'temp_change_c', 'change_north', 'change_south', 'change_global']

sns.pairplot(df[features].dropna(), height=2.5)

plt.tight_layout()
plt.show()