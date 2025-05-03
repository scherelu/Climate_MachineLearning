

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor, StackingRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import Ridge
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

# Initialize models with best hyperparameters
xgb = XGBRegressor(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42)
rf = RandomForestRegressor(n_estimators=200, max_depth=7, random_state=42)
gbr = GradientBoostingRegressor(n_estimators=400, max_depth=6, learning_rate=0.05, random_state=42)

voting = VotingRegressor(estimators=[
    ('xgb', xgb),
    ('rf', rf),
    ('gbr', gbr)
])

voting.fit(X_train, y_train)
y_pred_voting = voting.predict(X_test)

stacking = StackingRegressor(
    estimators=[
        ('xgb', xgb),
        ('rf', rf),
        ('gbr', gbr)
    ],
    final_estimator= XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1),
    passthrough=False
)

stacking.fit(X_train, y_train)
y_pred_stacking = stacking.predict(X_test)

# function to evaluate the passed data
def evaluate_model(name, y_pred, testing_df, target):
    testing_df_copy = testing_df.copy()
    testing_df_copy['y_pred'] = y_pred

    global_avg_pred = testing_df_copy.groupby('year')['y_pred'].mean()
    global_avg_true = testing_df_copy.groupby('year')[target].mean()

    mae = mean_absolute_error(global_avg_true, global_avg_pred)
    rmse = np.sqrt(mean_squared_error(global_avg_true, global_avg_pred))
    
    print(f"{name} Global MAE: {mae:.4f}")
    print(f"{name} Global RMSE: {rmse:.4f}")
    print("-" * 30)
    return mae, rmse

# print to compare performance of both ensemble algorithms
print("\n--- Ensemble Model Comparison ---\n")
mae_voting, rmse_voting = evaluate_model("VotingRegressor", y_pred_voting, testing_df, target)
mae_stacking, rmse_stacking = evaluate_model("StackingRegressor", y_pred_stacking, testing_df, target)

print("Summary:")
print(f"VotingRegressor, MAE: {mae_voting:.4f}, RMSE: {rmse_voting:.4f}")
print(f"StackingRegressor, MAE: {mae_stacking:.4f}, RMSE: {rmse_stacking:.4f}")