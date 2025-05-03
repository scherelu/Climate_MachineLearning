"""
This script implements the VotingRegressor ensemble method offered by scikit-learn
to analyze the annual climate dataset and visualize its performance.

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

# load annual data
annual = pd.read_csv("./data/annual/annual_data_trim.csv")

# scale year feature
min_year = annual['year'].min()
max_year = annual['year'].max()
year_range = max_year - min_year
annual['year_scaled'] = (annual['year'] - min_year) / year_range

# split train/test
training_df = annual[annual['year'] <= 2008]
testing_df = annual[annual['year'] > 2008]

features = [
    'year_scaled', 'co2_mean', 'co2_growth', 'ch4_mean', 'ch4_growth',
    'extent_global', 'area_global', 'extent_change_global', 'area_change_global'
]
target = 'temp_change_c'

X_train = training_df[features]
y_train = training_df[target]
X_test = testing_df[features]
y_test = testing_df[target]

X_train, y_train = shuffle(X_train, y_train, random_state=42)

# intialize
xgb = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42)
rf = RandomForestRegressor(n_estimators=200, max_depth=7, random_state=42)
gbr = GradientBoostingRegressor(n_estimators=400, max_depth=6, learning_rate=0.05, random_state=42)

voting = VotingRegressor(estimators=[
    ('xgb', xgb),
    ('rf', rf),
    ('gbr', gbr)
])

# train, predict
voting.fit(X_train, y_train)
y_pred_voting = voting.predict(X_test)

# eval
testing_df_copy = testing_df.copy()
testing_df_copy['y_pred'] = y_pred_voting

global_avg_pred = testing_df_copy.groupby('year')['y_pred'].mean()
global_avg_true = testing_df_copy.groupby('year')[target].mean()

mae = mean_absolute_error(global_avg_true, global_avg_pred)
rmse = np.sqrt(mean_squared_error(global_avg_true, global_avg_pred))

print("\n--- VotingRegressor Evaluation ---\n")
print(f"Global MAE: {mae:.4f}")
print(f"Global RMSE: {rmse:.4f}")


# line plot, global predictions vs. true values
plt.figure(figsize=(10, 6))
plt.plot(global_avg_true.index, global_avg_true.values, marker='o', label='True Global Avg')
plt.plot(global_avg_pred.index, global_avg_pred.values, marker='s', label='Predicted Global Avg')
plt.title('Global Average Temperature Change: True vs. Predicted')
plt.xlabel('Year')
plt.ylabel('Temperature Change (Celsius)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

# barplot, per year absolute error
per_year_error = abs(global_avg_true - global_avg_pred)
plt.figure(figsize=(10, 6))
sns.barplot(x=per_year_error.index, y=per_year_error.values)
plt.title('Per-Year Absolute Prediction Error')
plt.xlabel('Year')
plt.ylabel('Absolute Error (Celsius)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# scatterplot, predicted vs. true global average
plt.figure(figsize=(8, 6))
sns.scatterplot(x=global_avg_true, y=global_avg_pred)
plt.plot([global_avg_true.min(), global_avg_true.max()],
         [global_avg_true.min(), global_avg_true.max()],
         color='red', linestyle='--', label='Ideal')
plt.title('Predicted vs. True Global Average (Per Year)')
plt.xlabel('True Global Average (Celsius)')
plt.ylabel('Predicted Global Average (Celsius)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()