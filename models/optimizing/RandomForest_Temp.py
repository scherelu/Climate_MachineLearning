"""
This script implements the voting classifier ensemble method offered by the scikit-learn library to
analyze the annual data set

    - Author: Ludwig Scherer
    - Date: 05/01/2025
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# read in the datasets
annual = pd.read_csv("./data/annual/annual_data_trim.csv")
monthly = pd.read_csv("./data/monthly/monthly_data_trim.csv")

unique_countries = annual['country'].unique()

min_year = annual['year'].min()
max_year = annual['year'].max()
year_range = max_year - min_year

annual['year_scaled'] = (annual['year'] - min_year) / year_range

training_df = annual[annual['year'] <= 2008]
testing_df = annual[annual['year'] > 2008]

features = [
    'year_scaled', 'co2_mean', 'co2_growth', 'ch4_mean', 'ch4_growth', 'extent_global', 'area_global', 
    'extent_change_global', 'area_change_global'
]

target = 'temp_change_c'

X_train = training_df[features]
y_train = training_df[target]

X_test = testing_df[features]
y_test = testing_df[target]

X_train, y_train = shuffle(X_train, y_train, random_state=42)



# Define hyperparameter grids
n_estimators_list = [100, 200, 300, 400]
max_depth_list = [5, 6, 7, 8, 9]

# Initialize best scores
best_mae = np.inf
best_params = None

# Loop over combinations
for n_estimators in n_estimators_list:
    for max_depth in max_depth_list:
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)
        y_pred_country = model.predict(X_test)
        
        # Add predictions to test set
        testing_df_copy = testing_df.copy()
        testing_df_copy['y_pred'] = y_pred_country

        # Calculate global average
        global_avg_pred = testing_df_copy.groupby('year')['y_pred'].mean()
        global_avg_true = testing_df_copy.groupby('year')[target].mean()

        # Calculate metrics
        mae = mean_absolute_error(global_avg_true, global_avg_pred)
        rmse = np.sqrt(mean_squared_error(global_avg_true, global_avg_pred))

        print(f"n_estimators={n_estimators}, max_depth={max_depth}")
        print(f"Global MAE: {mae:.4f}, Global RMSE: {rmse:.4f}")
        print("------")

        # Track best model
        if mae < best_mae:
            best_mae = mae
            best_params = {
                'n_estimators': n_estimators,
                'max_depth': max_depth
            }

print("Best hyperparameters (RandomForestRegressor):")
print(best_params)
print(f"Best Global MAE: {best_mae:.4f}")
