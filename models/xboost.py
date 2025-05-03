import pandas as pd
import time
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

#loading the datasets
annual_df = pd.read_csv("./data/annual/annual_data_trim.csv")
monthly_df = pd.read_csv("./data/monthly/monthly_data_trim.csv")

# Import plotting functions and features from randomF.py
from models.randomF import plot_actual_vs_predicted, plot_feature_importance, features  # Import 'features' too


### Annual Data Model##
print(f'XGBoost Model on Annual Dataset')
X_annual = annual_df[features]
y_temp_annual = annual_df['temp_change_c']
y_absol_annual = annual_df['absol_temp_c']

# splitting data into training and testing sets
X_train_a, X_test_a, y_train_temp, y_test_temp = train_test_split(X_annual, y_temp_annual, test_size=0.2, random_state=42)
_, _, y_train_absol, y_test_absol = train_test_split(X_annual, y_absol_annual, test_size=0.2, random_state=42)

# Annual Temp Change Model (temp_change_c)
start_time_xgb_tc = time.time()
xgb_temp = xgb.XGBRegressor(n_estimators=100, random_state=42) # You can adjust parameters
xgb_temp.fit(X_train_a, y_train_temp)
y_pred_xgb_temp = xgb_temp.predict(X_test_a)
end_time_xgb_tc = time.time()
execution_time_xgb_tc = end_time_xgb_tc - start_time_xgb_tc
print("XGBoost Annual Temp Change - R2:", r2_score(y_test_temp, y_pred_xgb_temp))
print("XGBoost Annual Temp Change - MSE:", mean_squared_error(y_test_temp, y_pred_xgb_temp))
print(f"XGBoost Annual Temp Change - Execution Time: {execution_time_xgb_tc:.3f} seconds")

# Annual Absol Temp Model (absol_temp_c)
start_time_xgb_at = time.time()
xgb_absol = xgb.XGBRegressor(n_estimators=100, random_state=42)
xgb_absol.fit(X_train_a, y_train_absol)
y_pred_xgb_absol = xgb_absol.predict(X_test_a)
end_time_xgb_at = time.time()
execution_time_xgb_at = end_time_xgb_at - start_time_xgb_at
print("XGBoost Annual Absolute Temp - R2:", r2_score(y_test_absol, y_pred_xgb_absol))
print("XGBoost Annual Absolute Temp - MSE:", mean_squared_error(y_test_absol, y_pred_xgb_absol))
print(f"XGBoost Annual Absolute Temp - Execution Time: {execution_time_xgb_at:.3f} seconds")


#### Monthly Data Model##
print(f'XGBoost Model on Monthly Dataset')
X_monthly = monthly_df[features]
##* monthly_df doesnt have absol_temp_c, so fcusing on temp_change_c
y_temp_monthly = monthly_df["temp_change_c"]

# splitting data into training and testing sets
X_train_m, X_test_m, y_train_temp_m, y_test_temp_m = train_test_split(X_monthly, y_temp_monthly, test_size=0.2, random_state=42)

# Monthly Temp Change Model (temp_change_c)
start_time_xgb_mtc = time.time()
xgb_temp_m = xgb.XGBRegressor(n_estimators=100, random_state=42)
xgb_temp_m.fit(X_train_m, y_train_temp_m)
y_pred_xgb_temp_m = xgb_temp_m.predict(X_test_m)
end_time_xgb_mtc = time.time()
execution_time_xgb_mtc = end_time_xgb_mtc - start_time_xgb_mtc

print("XGBoost Monthly Temp Change - R2:", r2_score(y_test_temp_m, y_pred_xgb_temp_m))
print("XGBoost Monthly Temp Change - MSE:", mean_squared_error(y_test_temp_m, y_pred_xgb_temp_m))
print(f"XGBoost Monthly Temp Change - Execution Time: {execution_time_xgb_mtc:.3f} seconds")

# Plotting for XGBoost  #Added XGBoost plots
plot_actual_vs_predicted(y_test_temp, y_pred_xgb_temp, "Annual Temp Change", "XGBoost")
plot_actual_vs_predicted(y_test_absol, y_pred_xgb_absol, "Annual Absolute Temp", "XGBoost")

plot_feature_importance(xgb_temp, features, "Annual Temp Change", "XGBoost")
plot_feature_importance(xgb_absol, features, "Annual Absolute Temp", "XGBoost")

plot_actual_vs_predicted(y_test_temp_m, y_pred_xgb_temp_m, "Monthly", "XGBoost")
plot_feature_importance(xgb_temp_m, features, "Monthly", "XGBoost")