"""
This file is used to prepare and split the large amount of data contained in the ave_temp_change.csv
file. For exmple, countries that have too many missing years will be removed. This could be very young
countries, or countries which seized to exist (e.g. Soviet Union) and thus are represented in the 
dataset, but provide siginificantly less data than the others. All of the seasonal data entries will
be removed, since they are not compatible with the nature of the data contained in the other sets we
want to combine them with. Unwanted columns will also be removed. 

Original Dataset:

    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change

    - Author: Ludwig Scherer
    - Date: 04/15/2025

"""

import pandas as pd

temp_change_set = pd.read_csv("data/original/ave_temp_change.csv", header=0)

columns_to_keep = ['Area', 'Months', 'Year', 'Value']
temp_change_set = temp_change_set[columns_to_keep] # Remove unnecessary columns
temp_change_set.rename(columns={'Area': 'Country', 'Value': 'Temp_Change_C'}, inplace=True) # Rename Area column to country


# Extract annual data
temp_change_ann = temp_change_set[(temp_change_set['Months'] == 'Meteorological year')] 
temp_change_ann = temp_change_ann[['Country', 'Year', 'Temp_Change_C']] # get rid of month column

# This block is to clean the annual data. I.e. remove countries that are missing too many years of data
# group by country and check completeness
incomplete_countries = []
complete_countries = []

expected_years = set(range(1961,2021))

for country, group in temp_change_ann.groupby("Country"): # iterate of dataset grouped by country names
    years_present = set(group["Year"])
    missing_years = sorted(expected_years - years_present)
    if len(missing_years) < 10 : # if less than 10 years of data are missing
        group = group.sort_values("Year").copy()
        group["Temp_Change_C"] = group["Temp_Change_C"].interpolate() # interpolate the missing values
        complete_countries.append(group) # add country group to complete
    else: # if more than 10 years of data are missing
        incomplete_countries.append((country, len(missing_years), missing_years)) # add to incomplete

# create a dataframe of incomplete countries
incomplete_df = pd.DataFrame(incomplete_countries, columns=["Country", "Missing_Count", "Missing_Years"])
incomplete_df.to_csv("data/preprocessed/removed_countries_annual.csv", index=False)

# update annual data with complete data only
temp_change_ann = pd.concat(complete_countries).reset_index(drop=True)

# Extract monthly data
months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]
temp_change_mon = temp_change_set[temp_change_set['Months'].isin(months)]

# impose order on the months column
temp_change_mon = temp_change_mon.copy()
temp_change_mon['Months'] = pd.Categorical(temp_change_mon['Months'], categories=months, ordered=True)

# this block is to clean the monthly data. I.e. remove countries that are missing too many years of data
# group by country and check completeness
incomplete_countries = []
complete_countries = []

expected_years = set(range(1961,2021))

for country, group in temp_change_mon.groupby("Country"): # iterate of dataset grouped by country names
    years_present = set(group["Year"])
    missing_years = sorted(expected_years - years_present)
    if len(missing_years) < 10 : # if less than 10 years of data are missing
        interpolated_months = []
        for month, month_group in group.groupby("Months", observed=False):
            
            month_group = month_group.sort_values("Year").copy()
            month_group["Temp_Change_C"] = month_group["Temp_Change_C"].interpolate() # interpolate the missing values
            interpolated_months.append(month_group) # add month group to complete
        complete_country = pd.concat(interpolated_months)
        complete_countries.append(complete_country)
        
    else: # if more than 10 years of data are missing
        incomplete_countries.append((country, len(missing_years), missing_years)) # add to incomplete

# create a dataframe of incomplete countries
incomplete_df = pd.DataFrame(incomplete_countries, columns=["Country", "Missing_Count", "Missing_Years"])
incomplete_df.to_csv("data/preprocessed/removed_countries_monthly.csv", index=False)

# update monthly data with complete data only
temp_change_mon = pd.concat(complete_countries).reset_index(drop=True)

# round temperature anomaly values to 3 decimal places
temp_change_ann['Temp_Change_C'] = round(temp_change_ann['Temp_Change_C'], 4)
temp_change_mon['Temp_Change_C'] = round(temp_change_mon['Temp_Change_C'], 4)

# map to convert categorical month values to numerical
month_name_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

# map the categorical month values to numerical
temp_change_mon["Month_Num"] = temp_change_mon["Months"].map(month_name_map)

# impose order on the numerical months column
month_order = list(month_name_map.values())
temp_change_mon["Month_Num"] = pd.Categorical(
    temp_change_mon["Month_Num"],
    categories=month_order,
    ordered=True
)

# impose order on the categorical months column
month_order = list(month_name_map.keys())
temp_change_mon["Months"] = pd.Categorical(
    temp_change_mon["Months"],
    categories=month_order,
    ordered=True
)

temp_change_mon.rename(columns={'Months': 'month_cat', 'Month_Num': 'month'}, inplace=True)

temp_change_ann.columns = temp_change_ann.columns.str.lower()
temp_change_mon.columns = temp_change_mon.columns.str.lower()

# store cleaned datasets
temp_change_ann.to_csv("data/preprocessed/annual_clean.csv", index=False)
temp_change_mon.to_csv("data/preprocessed/monthly_clean.csv", index=False)