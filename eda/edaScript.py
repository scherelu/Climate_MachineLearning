import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# loading the Datasets
annual_df = pd.read_csv("./data/annual/annual_data.csv")
month_df = pd.read_csv("./data/monthly/monthly_data.csv")

# Shape & basic info
print("Annual Data Shape:")
print(annual_df.shape)
print(annual_df.info())

print("\nMonthly Data Shape:")
print(month_df.shape)
print(month_df.info())

# First few rows
print(annual_df.head())
print(month_df.head())

# checking for missing data
print("Annual missing values:\n", annual_df.isnull().sum())
print("Monthly missing values:\n", month_df.isnull().sum())

print("Annual Summary Description:")
print(annual_df.describe())

print("\nMonthly Summary Description:")
print(month_df.describe())



# VISUALIZATIONS
# histograms
annual_df.hist(figsize=(12, 8))
plt.suptitle("Annual Data Distributions")
plt.tight_layout()
plt.show()

month_df.hist(figsize=(12, 8))
plt.suptitle("Monthly Data Distributions")
plt.tight_layout()
plt.show()


# Missing Value Analysis (Visualization) 

### visualizations for missing values (Count)
annual_missing = annual_df.isnull().sum()
annual_missing = annual_missing[annual_missing > 0].sort_values(ascending=False)
monthly_missing = month_df.isnull().sum()
monthly_missing = monthly_missing[monthly_missing > 0].sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=annual_missing.index, y=annual_missing.values)
plt.title('Missing Values in Annual Data (Count)')
plt.xlabel('Columns')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(x=monthly_missing.index, y=monthly_missing.values)
plt.title('Missing Values in Monthly Data (Count)')
plt.xlabel('Columns')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

### visualizations for missing values (Percentage)
##percentage of entries that are missing out of the total number of entries in that column
annual_missing_percent = (annual_df.isnull().sum() / len(annual_df)) * 100
annual_missing_percent = annual_missing_percent[annual_missing_percent > 0].sort_values(ascending=False)
monthly_missing_percent = (month_df.isnull().sum() / len(month_df)) * 100
monthly_missing_percent = monthly_missing_percent[monthly_missing_percent > 0].sort_values(ascending=False)


plt.figure(figsize=(10, 6))
sns.barplot(x=annual_missing_percent.index, y=annual_missing_percent.values)
plt.title('Percentage of Missing Values in Annual Data')
plt.xlabel('Columns')
plt.ylabel('Percentage of Missing Values (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(x=monthly_missing_percent.index, y=monthly_missing_percent.values)
plt.title('Percentage of Missing Values in Monthly Data')
plt.xlabel('Columns')
plt.ylabel('Percentage of Missing Values (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
