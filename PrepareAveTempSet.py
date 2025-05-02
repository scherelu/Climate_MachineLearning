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

temp_change_set['Country'] = temp_change_set['Country'].replace({'R?union': 'Reunion', "C?te d'Ivoire": "Cote d'Ivoire"})

# this map was created using ChatGPT
# this was the prompt:please create a mapping for all country names contained in this list, so that it can be applied in a python 
# script to create a new feature column for each country called 'hemisphere', depending on which hemisphere 
# the associated country is located in
# Costa Rica, Ivory Coast, Reunion, Equatorial Guinea, and Cuba had to be added manually
country_to_hemisphere = {
    # Northern Hemisphere
    'Afghanistan': 'north', 'Albania': 'north', 'Algeria': 'north', 'Andorra': 'north',
    'Armenia': 'north', 'Austria': 'north', 'Bahamas': 'north', 'Bahrain': 'north',
    'Bangladesh': 'north', 'Barbados': 'north', 'Belize': 'north', 'Bermuda': 'north',
    'Bhutan': 'north', 'Bulgaria': 'north', 'Canada': 'north', 'China': 'north',
    'China, Hong Kong SAR': 'north', 'China, Macao SAR': 'north', 'China, Taiwan Province of': 'north',
    'China, mainland': 'north', 'Costa Rica' : 'north', "Cote d'Ivoire": 'north', 'Cuba': 'north', 'Cyprus': 'north', 'Czech Republic': 'north', 'Denmark': 'north',
    'Dominican Republic': 'north', 'Egypt': 'north', 'El Salvador': 'north', 'Estonia': 'north', 'Equatorial Guinea': 'north',
    'France': 'north', 'Germany': 'north', 'Greece': 'north', 'Greenland': 'north',
    'Guatemala': 'north', 'Honduras': 'north', 'Hungary': 'north', 'Iceland': 'north',
    'India': 'north', 'Iran (Islamic Republic of)': 'north', 'Iraq': 'north', 'Ireland': 'north',
    'Israel': 'north', 'Italy': 'north', 'Jamaica': 'north', 'Japan': 'north', 'Jordan': 'north',
    'Kuwait': 'north', 'Latvia': 'north', 'Lebanon': 'north', 'Lithuania': 'north',
    'Luxembourg': 'north', 'Malta': 'north', 'Mexico': 'north', 'Moldova': 'north',
    'Monaco': 'north', 'Mongolia': 'north', 'Montenegro': 'north', 'Morocco': 'north',
    'Nepal': 'north', 'Netherlands': 'north', 'North Korea': 'north', 'Norway': 'north',
    'Oman': 'north', 'Pakistan': 'north', 'Panama': 'north', 'Philippines': 'north',
    'Poland': 'north', 'Portugal': 'north', 'Puerto Rico': 'north', 'Qatar': 'north',
    'Republic of Korea': 'north', 'Reunion': 'south', 'Romania': 'north', 'Russian Federation': 'north',
    'San Marino': 'north', 'Saudi Arabia': 'north', 'Serbia': 'north', 'Singapore': 'north',
    'Slovakia': 'north', 'Slovenia': 'north', 'South Korea': 'north', 'Spain': 'north',
    'Sri Lanka': 'north', 'Sudan': 'north', 'Sweden': 'north', 'Switzerland': 'north',
    'Syrian Arab Republic': 'north', 'Thailand': 'north', 'Tunisia': 'north', 'Turkey': 'north',
    'Turkmenistan': 'north', 'Ukraine': 'north', 'United Arab Emirates': 'north',
    'United Kingdom of Great Britain and Northern Ireland': 'north', 'United States of America': 'north',
    'Uzbekistan': 'north', 'Viet Nam': 'north', 'Western Sahara': 'north', 'Yemen': 'north',

    # Southern Hemisphere
    'Angola': 'south', 'Argentina': 'south', 'Australia': 'south', 'Bolivia (Plurinational State of)': 'south',
    'Botswana': 'south', 'Brazil': 'south', 'Chile': 'south', 'Colombia': 'south',
    'Congo': 'south', 'Democratic Republic of the Congo': 'south', 'Ecuador': 'south',
    'Fiji': 'south', 'French Guyana': 'south', 'French Polynesia': 'south', 'Gabon': 'south',
    'Guyana': 'south', 'Indonesia': 'south', 'Kenya': 'south', 'Madagascar': 'south',
    'Malawi': 'south', 'Mauritius': 'south', 'Mozambique': 'south', 'Namibia': 'south',
    'New Zealand': 'south', 'Papua New Guinea': 'south', 'Paraguay': 'south', 'Peru': 'south',
    'Rwanda': 'south', 'Seychelles': 'south', 'South Africa': 'south', 'Suriname': 'south',
    'Tanzania': 'south', 'Timor-Leste': 'south', 'Uganda': 'south', 'Uruguay': 'south',
    'Vanuatu': 'south', 'Venezuela (Bolivarian Republic of)': 'south', 'Zambia': 'south',
    'Zimbabwe': 'south',

    # Equatorial / Special
    'American Samoa': 'south', 'Anguilla': 'north', 'Antarctica': 'south',
    'Antigua and Barbuda': 'north', 'Aruba': 'north', 'Bahamas': 'north', 'Barbados': 'north',
    'Belize': 'north', 'Benin': 'north', 'Bhutan': 'north', 'British Virgin Islands': 'north',
    'Brunei Darussalam': 'north', 'Burkina Faso': 'north', 'Burundi': 'south',
    "Côte d'Ivoire": 'north', 'Cabo Verde': 'north', 'Cambodia': 'north', 'Cameroon': 'north',
    'Cayman Islands': 'north', 'Central African Republic': 'north', 'Chad': 'north',
    'Channel Islands': 'north', 'Christmas Island': 'south', 'Cocos (Keeling) Islands': 'south',
    'Comoros': 'south', 'Cook Islands': 'south', 'Cyprus': 'north', "Democratic People's Republic of Korea": 'north',
    'Djibouti': 'north', 'Dominica': 'north', 'Eswatini': 'south', 'Falkland Islands (Malvinas)': 'south',
    'Faroe Islands': 'north', 'Finland': 'north', 'French Southern Territories': 'south',
    'Gambia': 'north', 'Ghana': 'north', 'Gibraltar': 'north', 'Grenada': 'north',
    'Guadeloupe': 'north', 'Guinea': 'north', 'Guinea-Bissau': 'north', 'Haiti': 'north',
    'Holy See': 'north', 'Isle of Man': 'north', 'Kiribati': 'south', 'Lao People\'s Democratic Republic': 'north',
    'Lebanon': 'north', 'Lesotho': 'south', 'Liberia': 'north', 'Libya': 'north',
    'Liechtenstein': 'north', 'Malaysia': 'north', 'Maldives': 'north', 'Mali': 'north',
    'Malta': 'north', 'Martinique': 'north', 'Mauritania': 'north', 'Mayotte': 'south',
    'Midway Island': 'north', 'Monaco': 'north', 'Mongolia': 'north', 'Montserrat': 'north',
    'Myanmar': 'north', 'Nauru': 'south', 'Netherlands Antilles (former)': 'north',
    'New Caledonia': 'south', 'Nicaragua': 'north', 'Niger': 'north', 'Nigeria': 'north',
    'Niue': 'south', 'Norfolk Island': 'south', 'Palestine': 'north', 'Philippines': 'north',
    'Pitcairn': 'south', 'Réunion': 'south', 'Saint Helena, Ascension and Tristan da Cunha': 'south',
    'Saint Kitts and Nevis': 'north', 'Saint Lucia': 'north', 'Saint Pierre and Miquelon': 'north',
    'Saint Vincent and the Grenadines': 'north', 'Samoa': 'south', 'San Marino': 'north',
    'Sao Tome and Principe': 'north', 'Senegal': 'north', 'Seychelles': 'south',
    'Sierra Leone': 'north', 'Solomon Islands': 'south', 'Somalia': 'north',
    'South Georgia and the South Sandwich Islands': 'south', 'Sudan (former)': 'north',
    'Svalbard and Jan Mayen Islands': 'north', 'Togo': 'north', 'Tokelau': 'south',
    'Tonga': 'south', 'Trinidad and Tobago': 'north', 'Turks and Caicos Islands': 'north',
    'Tuvalu': 'south', 'United Republic of Tanzania': 'south', 'United States Virgin Islands': 'north',
    'Wake Island': 'north', 'Wallis and Futuna Islands': 'south', 'Western Sahara': 'north',
    'Yemen': 'north'
}

temp_change_set['hemisphere'] = temp_change_set['Country'].map(country_to_hemisphere)

# Extract annual data
temp_change_ann = temp_change_set[(temp_change_set['Months'] == 'Meteorological year')] 
temp_change_ann = temp_change_ann[['Country', 'Year', 'Temp_Change_C', 'hemisphere']] # get rid of month column

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

nan_count_ann = temp_change_ann['hemisphere'].isna().sum()
nan_count_mon = temp_change_mon['hemisphere'].isna().sum()

print(nan_count_ann, nan_count_mon)

# store cleaned datasets
temp_change_ann.to_csv("data/preprocessed/annual_clean.csv", index=False)
temp_change_mon.to_csv("data/preprocessed/monthly_clean.csv", index=False)