import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# load data
annual_df = pd.read_csv("data/annual/annual_data_trim.csv")
monthly_df = pd.read_csv("data/monthly/monthly_data_trim.csv")

# annual data regression
annual_data = annual_df.dropna(subset=["co2_mean", "ch4_mean", "temp_change_c"])
X_annual = annual_data[["co2_mean", "ch4_mean"]]
y_annual = annual_data["temp_change_c"]

X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(X_annual, y_annual, test_size=0.2, random_state=42)
model_annual = LinearRegression()
model_annual.fit(X_train_a, y_train_a)
y_pred_a = model_annual.predict(X_test_a)

print("=== Annual Data Linear Regression ===")
print("Coefficients:", dict(zip(X_annual.columns, model_annual.coef_)))
print("Intercept:", model_annual.intercept_)
print("MSE:", mean_squared_error(y_test_a, y_pred_a))
print("R_squared:", r2_score(y_test_a, y_pred_a))

# monthly regression
monthly_data = monthly_df.dropna(subset=["co2_average", "ch4_average", "temp_change_c"])
X_monthly = monthly_data[["co2_average", "ch4_average"]]
y_monthly = monthly_data["temp_change_c"]

X_train_m, X_test_m, y_train_m, y_test_m = train_test_split(X_monthly, y_monthly, test_size=0.2, random_state=42)
model_monthly = LinearRegression()
model_monthly.fit(X_train_m, y_train_m)
y_pred_m = model_monthly.predict(X_test_m)

print("\n=== Monthly Data Linear Regression ===")
print("Coefficients:", dict(zip(X_monthly.columns, model_monthly.coef_)))
print("Intercept:", model_monthly.intercept_)
print("MSE:", mean_squared_error(y_test_m, y_pred_m))
print("R_squared:", r2_score(y_test_m, y_pred_m))

# plots
sns.set_theme(style="whitegrid", context="notebook")

# annual
plt.figure(figsize=(10, 5))
sns.scatterplot(x=y_test_a, y=y_pred_a, color='blue')
plt.plot([y_test_a.min(), y_test_a.max()], [y_test_a.min(), y_test_a.max()], 'k--')
plt.xlabel("Actual Temperature Change (C)")
plt.ylabel("Predicted Temperature Change (C)")
plt.title("Annual Data: Actual vs Predicted")
plt.savefig("models/plots/annual_regression_plot.png")
plt.close()

# monthly plot
plt.figure(figsize=(10, 5))
sns.scatterplot(x=y_test_m, y=y_pred_m, color='green')
plt.plot([y_test_m.min(), y_test_m.max()], [y_test_m.min(), y_test_m.max()], 'k--')
plt.xlabel("Actual Temperature Change (C)")
plt.ylabel("Predicted Temperature Change (C)")
plt.title("Monthly Data: Actual vs Predicted")
plt.savefig("models/plots/monthly_regression_plot.png")
plt.close()