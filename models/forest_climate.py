import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# seaborn styling
sns.set_theme(style="whitegrid", context="notebook")

# load datasets
annual_df = pd.read_csv("data/annual/annual_data_trim.csv")
monthly_df = pd.read_csv("data/monthly/monthly_data_trim.csv")

# ============= annual data
print("\n--- Random Forest on Annual Data ---")
annual_data = annual_df.dropna(subset=["co2_mean", "ch4_mean", "extent_global", "temp_change_c"])
X_annual = annual_data[["co2_mean", "ch4_mean", "extent_global"]]
y_annual = annual_data["temp_change_c"]

X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(X_annual, y_annual, test_size=0.2, random_state=42)

rf_annual = RandomForestRegressor(n_estimators=100, random_state=42)
rf_annual.fit(X_train_a, y_train_a)
y_pred_rf_a = rf_annual.predict(X_test_a)

print("R_squared:", r2_score(y_test_a, y_pred_rf_a))
print("MSE:", mean_squared_error(y_test_a, y_pred_rf_a))

# plot for annual data
plt.figure(figsize=(10, 5))
sns.scatterplot(x=y_test_a, y=y_pred_rf_a, color='blue')
plt.plot([y_test_a.min(), y_test_a.max()], [y_test_a.min(), y_test_a.max()], 'k--')
plt.xlabel("Actual Temperature Change (C)")
plt.ylabel("Predicted Temperature Change (C)")
plt.title("Annual Data: Actual vs Predicted (Random Forest)")
plt.show()

# ============= monthly
print("\n--- Random Forest on Monthly Data ---")
monthly_data = monthly_df.dropna(subset=["co2_average", "ch4_average", "extent_global", "temp_change_c"])
X_monthly = monthly_data[["co2_average", "ch4_average", "extent_global"]]
y_monthly = monthly_data["temp_change_c"]

X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(X_monthly, y_monthly, test_size=0.2, random_state=42)

rf_monthly = RandomForestRegressor(n_estimators=100, random_state=42)
rf_monthly.fit(X_train_m, y_train_m)
y_pred_rf_m = rf_monthly.predict(X_test_m)

print("R_squared:", r2_score(y_test_m, y_pred_rf_m))
print("MSE:", mean_squared_error(y_test_m, y_pred_rf_m))

# plot monthly
plt.figure(figsize=(10, 5))
sns.scatterplot(x=y_test_m, y=y_pred_rf_m, color='green')
plt.plot([y_test_m.min(), y_test_m.max()], [y_test_m.min(), y_test_m.max()], 'k--')
plt.xlabel("Actual Temperature Change (C)")
plt.ylabel("Predicted Temperature Change (C)")
plt.title("Monthly Data: Actual vs Predicted (Random Forest)")
plt.show()
