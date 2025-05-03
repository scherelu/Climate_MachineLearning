"""
This script implements the VotingRegressor ensemble method offered by scikit-learn
to analyze the monthly climate dataset and visualize the results.

- Author: Ludwig Scherer
- Date: 05/02/2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from xgboost import XGBRegressor
from sklearn.utils import shuffle
from sklearn.metrics import mean_absolute_error, mean_squared_error

# load data
monthly = pd.read_csv("./data/monthly/monthly_data_trim.csv")

# convert categorical features to numerical
monthly['country_code'] = monthly['country'].astype('category').cat.codes
monthly['hemisphere_code'] = monthly['hemisphere'].astype('category').cat.codes


# split data
training_df = monthly[monthly['year'] <= 2008]
testing_df = monthly[monthly['year'] > 2008]

features = [
    'hemisphere_code', 'country_code', 'decimal_date', 'co2_mean', 'co2_growth', 'ch4_mean', 'ch4_growth',
    'extent_global', 'area_global', 'extent_change_global', 'area_change_global'
]

target = 'temp_change_c'

X_train = training_df[features]
y_train = training_df[target]
X_test = testing_df[features]
y_test = testing_df[target]

X_train, y_train = shuffle(X_train, y_train, random_state=42)

# intializations
xgb = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42)
rf = RandomForestRegressor(n_estimators=200, max_depth=7, random_state=42)
gbr = GradientBoostingRegressor(n_estimators=400, max_depth=6, learning_rate=0.05, random_state=42)

voting = VotingRegressor(estimators=[
    ('xgb', xgb),
    ('rf', rf),
    ('gbr', gbr)
])

# train + predict
voting.fit(X_train, y_train)
y_pred_voting = voting.predict(X_test)

# eval
testing_df_copy = testing_df.copy()
testing_df_copy['y_pred'] = y_pred_voting

# get country level predictions
country_avg_pred = testing_df_copy.groupby('country')['y_pred'].mean()
country_avg_true = testing_df_copy.groupby('country')[target].mean()

# create dataframe for the country ranking
ranking_df = pd.DataFrame({
    'True Avg Temp Change': country_avg_true,
    'Predicted Avg Temp Change': country_avg_pred
}).sort_values('Predicted Avg Temp Change', ascending=False).reset_index()

print("\n--- Top 10 Countries (Highest Predicted Temp Change) ---")
print(ranking_df.head(10))

print("\n--- Bottom 10 Countries (Lowest Predicted Temp Change) ---")
print(ranking_df.tail(10))

# global metrics
global_avg_pred = testing_df_copy.groupby('year')['y_pred'].mean()
global_avg_true = testing_df_copy.groupby('year')[target].mean()

mae = mean_absolute_error(global_avg_true, global_avg_pred)
rmse = np.sqrt(mean_squared_error(global_avg_true, global_avg_pred))

print("\n--- VotingRegressor Global Evaluation ---")
print(f"Global MAE: {mae:.4f}")
print(f"Global RMSE: {rmse:.4f}")

# top 10 bar plot
top10 = ranking_df.head(10)
sns.barplot(
    x='Predicted Avg Temp Change',
    y='country',
    data=top10,
    palette='Reds_r'
)
plt.title('Top 10 Countries: Highest Predicted Avg Temp Change')
plt.xlabel('Predicted Avg Temp Change (Celsius)')
plt.ylabel('Country')
plt.show()

# bottom 10 bar plot
bottom10 = ranking_df.tail(10)
sns.barplot(
    x='Predicted Avg Temp Change',
    y='country',
    data=bottom10,
    palette='Blues'
)

plt.title('Bottom 10 Countries: Lowest Predicted Avg Temp Change')
plt.xlabel('Predicted Avg Temp Change (Celsius)')
plt.ylabel('Country')
plt.show()

# Scatter plot: predicted vs. true avg temp change per country
plt.figure(figsize=(8, 6))
sns.scatterplot(x=ranking_df['True Avg Temp Change'], y=ranking_df['Predicted Avg Temp Change'])
plt.plot(
    [ranking_df['True Avg Temp Change'].min(), ranking_df['True Avg Temp Change'].max()],
    [ranking_df['True Avg Temp Change'].min(), ranking_df['True Avg Temp Change'].max()],
    color='red', linestyle='--', label='Ideal'
)
plt.title('Predicted vs. True Avg Temp Change (Per Country)')
plt.xlabel('True Avg Temp Change (Celsius)')
plt.ylabel('Predicted Avg Temp Change (Celsius)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
