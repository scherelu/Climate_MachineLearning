import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

#loading the datasets
annual_df = pd.read_csv("./data/annual/annual_data_trim.csv")
monthly_df = pd.read_csv("./data/monthly/monthly_data_trim.csv")
print("Monthly dataset columns:", monthly_df.columns.tolist())

features = [
    'year', 'co2_mean', 'co2_growth',
    'ch4_mean', 'ch4_growth',
    'extent_global', 'extent_change_global',
    'area_global', 'area_change_global'
]

## Annual Data Model##
print(f'Random Forest Model on Annual Dataset')
X_annual = annual_df[features]
y_temp_annual = annual_df['temp_change_c']
y_absol_annual = annual_df['absol_temp_c']

# splitting data into training and testing sets 
X_train_a, X_test_a, y_train_temp, y_test_temp = train_test_split(X_annual, y_temp_annual, test_size=0.2, random_state=42)
_, _, y_train_absol, y_test_absol = train_test_split(X_annual, y_absol_annual, test_size=0.2, random_state=42)

# Annual Temp Change Model (temp_change_c)
start_time_tc = time.time()
rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
rf_temp.fit(X_train_a, y_train_temp)
y_pred_temp = rf_temp.predict(X_test_a)
end_time_tc = time.time()
execution_time_tc = end_time_tc - start_time_tc
print("Annual Temp Change - R2:", r2_score(y_test_temp, y_pred_temp))
print("Annual Temp Change - MSE:", mean_squared_error(y_test_temp, y_pred_temp))
print(f"Annual Absolute Temp - Execution Time: {execution_time_tc:.3f} seconds")


# Annual Absol Temp Model (absol_temp_c)
start_time_at = time.time()
rf_absol = RandomForestRegressor(n_estimators=100, random_state=42)
rf_absol.fit(X_train_a, y_train_absol)
y_pred_absol = rf_absol.predict(X_test_a)
end_time_at = time.time()
execution_time_at = end_time_at - start_time_at
print("Annual Absolute Temp - R2:", r2_score(y_test_absol, y_pred_absol))
print("Annual Absolute Temp - MSE:", mean_squared_error(y_test_absol, y_pred_absol))
print(f"Annual Absolute Temp - Execution Time: {execution_time_at:.3f} seconds")


#### Monthly Data Model##
print(f'Random Forest Model on Monthly Dataset')
X_monthly = monthly_df[features]
print(monthly_df.columns)
##* monthly_df doesnt have absol_temp_c, so fcusing on temp_change_c
y_temp_monthly = monthly_df["temp_change_c"]

# splitting data into training and testing sets 
X_train_m, X_test_m, y_train_temp_m, y_test_temp_m = train_test_split(X_monthly, y_temp_monthly, test_size=0.2, random_state=42)

# Monthly Temp Change Model (temp_change_c)
start_time_mtc = time.time()
rf_temp_m = RandomForestRegressor(n_estimators=100, random_state=42)
rf_temp_m.fit(X_train_m, y_train_temp_m)
y_pred_temp_m = rf_temp_m.predict(X_test_m)
end_time_mtc = time.time()
execution_time_mtc = end_time_mtc - start_time_mtc

print("Monthly Temp Change - R2:", r2_score(y_test_temp_m, y_pred_temp_m))
print("Monthly Temp Change - MSE:", mean_squared_error(y_test_temp_m, y_pred_temp_m))
print(f"Monthly Temp Change - Execution Time: {execution_time_mtc:.3f} seconds")

## Plotting ###
def plot_actual_vs_predicted(actual, predicted, data_type, model_name=""):
    # a scatter plot of actual vs. predicted values.
    plt.figure(figsize=(8, 6))
    plt.scatter(actual, predicted)
    plt.plot([np.min(actual), np.max(actual)], [np.min(actual), np.max(actual)], 'k--')  
    plt.xlabel("Actual Temperature Change (Celcius)")
    plt.ylabel("Predicted Temperature Change (Celcius)")
    plt.title(f"{model_name} ({data_type} Data): Actual vs. Predicted")
    plt.show()

def plot_feature_importance(model, feature_names, data_type, model_name=""):
    # a feature importance plot for a Random Forest model.
    importance = model.feature_importances_
    feature_importance = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
    feature_importance = feature_importance.sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['Feature'], feature_importance['Importance'])
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.title(f"{model_name} ({data_type} Data): Feature Importance")
    plt.show()

plot_actual_vs_predicted(y_test_temp, y_pred_temp, "Annual Temp Change", "Random Forest")
plot_actual_vs_predicted(y_test_absol, y_pred_absol, "Annual Absolute Temp", "Random Forest")

plot_feature_importance(rf_temp, features, "Annual Temp Change", "Random Forest")
plot_feature_importance(rf_absol, features, "Annual Absolute Temp", "Random Forest")

plot_actual_vs_predicted(y_test_temp_m, y_pred_temp_m, "Monthly", "Random Forest")
plot_feature_importance(rf_temp_m, features, "Monthly", "Random Forest")


