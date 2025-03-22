"""
Author: Ludwig Scherer
Date: 03/18/2025

This is the data manipulation file for our semester project. Here we extend and reshape the data 
from the Kaggle dataset, to include features that might be of interest to our analysis
found under: https://www.kaggle.com/datasets/goyaladi/climate-insights-dataset?resource=download&select=climate_change_data.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

data = pd.read_csv("modified_climate_change_data.csv", header=0)

tropical_locs = data[(data["Temperature"] > 25) & (data["Precipitation"] > 70) & (data["Humidity"] > 70)]
print(tropical_locs)


climate_features = data[['Temperature', 'Precipitation', 'Humidity']]

sc = StandardScaler()
scaled_features = sc.fit_transform(climate_features)

kmeans = KMeans(n_clusters= 5, random_state= 42)
data["Climate Cluster"] = kmeans.fit_predict(scaled_features)

cluster_summary = data.groupby("Climate Cluster")[climate_features.columns].mean()
print(cluster_summary)

print(data["Temperature"].max())


## This block was used to add a 'Continent' column to the dataset 
## define a mapping of countries to continents
# country_to_continent = {
#     # North America
#     "Canada": "North America", "United States of America": "North America", "Mexico": "North America",
#     "Greenland": "North America", "Bermuda": "North America", "Saint Pierre and Miquelon": "North America",
#     "United States Virgin Islands": "North America", "British Virgin Islands": "North America",
#     "Cayman Islands": "North America", "Bahamas": "North America", "Turks and Caicos Islands": "North America",

#     # South America
#     "Argentina": "South America", "Bolivia": "South America", "Brazil": "South America", "Chile": "South America",
#     "Colombia": "South America", "Ecuador": "South America", "Guyana": "South America", "Paraguay": "South America",
#     "Peru": "South America", "Suriname": "South America", "Uruguay": "South America", "Venezuela": "South America",
#     "French Guiana": "South America",

#     # Europe
#     "United Kingdom": "Europe", "Germany": "Europe", "France": "Europe", "Italy": "Europe", "Spain": "Europe",
#     "Portugal": "Europe", "Netherlands": "Europe", "Belgium": "Europe", "Switzerland": "Europe", "Austria": "Europe",
#     "Denmark": "Europe", "Sweden": "Europe", "Norway": "Europe", "Finland": "Europe", "Iceland": "Europe",
#     "Ireland": "Europe", "Luxembourg": "Europe", "Liechtenstein": "Europe", "Monaco": "Europe", "Andorra": "Europe",
#     "San Marino": "Europe", "Malta": "Europe", "Greece": "Europe", "Poland": "Europe", "Czech Republic": "Europe",
#     "Slovakia (Slovak Republic)": "Europe", "Hungary": "Europe", "Romania": "Europe", "Bulgaria": "Europe",
#     "Serbia": "Europe", "Montenegro": "Europe", "Bosnia and Herzegovina": "Europe", "Croatia": "Europe",
#     "Slovenia": "Europe", "Albania": "Europe", "Moldova": "Europe", "Lithuania": "Europe", "Latvia": "Europe",
#     "Estonia": "Europe", "Ukraine": "Europe", "Belarus": "Europe", "North Macedonia": "Europe",
#     "Faroe Islands": "Europe", "Guernsey": "Europe", "Jersey": "Europe", "Isle of Man": "Europe",
#     "Gibraltar": "Europe", "Svalbard & Jan Mayen Islands": "Europe",

#     # Africa
#     "Algeria": "Africa", "Angola": "Africa", "Benin": "Africa", "Botswana": "Africa", "Burkina Faso": "Africa",
#     "Burundi": "Africa", "Cape Verde": "Africa", "Cameroon": "Africa", "Central African Republic": "Africa",
#     "Chad": "Africa", "Comoros": "Africa", "Congo": "Africa", "Djibouti": "Africa", "Egypt": "Africa",
#     "Equatorial Guinea": "Africa", "Eritrea": "Africa", "Eswatini": "Africa", "Ethiopia": "Africa",
#     "Gabon": "Africa", "Gambia": "Africa", "Ghana": "Africa", "Guinea": "Africa", "Guinea-Bissau": "Africa",
#     "Ivory Coast": "Africa", "Kenya": "Africa", "Lesotho": "Africa", "Liberia": "Africa", "Libya": "Africa",
#     "Madagascar": "Africa", "Malawi": "Africa", "Mali": "Africa", "Mauritania": "Africa", "Mauritius": "Africa",
#     "Mayotte": "Africa", "Morocco": "Africa", "Mozambique": "Africa", "Namibia": "Africa", "Niger": "Africa",
#     "Nigeria": "Africa", "Reunion": "Africa", "Rwanda": "Africa", "Sao Tome and Principe": "Africa",
#     "Senegal": "Africa", "Seychelles": "Africa", "Sierra Leone": "Africa", "Somalia": "Africa",
#     "South Africa": "Africa", "South Sudan": "Africa", "Sudan": "Africa", "Tanzania": "Africa",
#     "Togo": "Africa", "Tunisia": "Africa", "Uganda": "Africa", "Zambia": "Africa", "Zimbabwe": "Africa",
#     "Western Sahara": "Africa",

#     # Asia
#     "Afghanistan": "Asia", "Armenia": "Asia", "Azerbaijan": "Asia", "Bahrain": "Asia", "Bangladesh": "Asia",
#     "Bhutan": "Asia", "Brunei Darussalam": "Asia", "Cambodia": "Asia", "China": "Asia", "Cyprus": "Asia",
#     "Georgia": "Asia", "India": "Asia", "Indonesia": "Asia", "Iran": "Asia", "Iraq": "Asia", "Israel": "Asia",
#     "Japan": "Asia", "Jordan": "Asia", "Kazakhstan": "Asia", "Kuwait": "Asia", "Kyrgyz Republic": "Asia",
#     "Lao People's Democratic Republic": "Asia", "Lebanon": "Asia", "Malaysia": "Asia", "Maldives": "Asia",
#     "Mongolia": "Asia", "Myanmar": "Asia", "Nepal": "Asia", "North Korea": "Asia", "Oman": "Asia",
#     "Pakistan": "Asia", "Palestinian Territory": "Asia", "Philippines": "Asia", "Qatar": "Asia",
#     "Saudi Arabia": "Asia", "Singapore": "Asia", "South Korea": "Asia", "Sri Lanka": "Asia",
#     "Syrian Arab Republic": "Asia", "Tajikistan": "Asia", "Thailand": "Asia", "Timor-Leste": "Asia",
#     "Turkmenistan": "Asia", "United Arab Emirates": "Asia", "Uzbekistan": "Asia", "Vietnam": "Asia",
#     "Yemen": "Asia", "Hong Kong": "Asia", "Macao": "Asia",

#     # Oceania
#     "Australia": "Oceania", "New Zealand": "Oceania", "Fiji": "Oceania", "Kiribati": "Oceania",
#     "Marshall Islands": "Oceania", "Micronesia": "Oceania", "Nauru": "Oceania", "Palau": "Oceania",
#     "Papua New Guinea": "Oceania", "Samoa": "Oceania", "Solomon Islands": "Oceania", "Tonga": "Oceania",
#     "Tuvalu": "Oceania", "Vanuatu": "Oceania", "Norfolk Island": "Oceania", "New Caledonia": "Oceania",
#     "Cook Islands": "Oceania", "Niue": "Oceania", "Pitcairn Islands": "Oceania", "Tokelau": "Oceania",
#     "Wallis and Futuna": "Oceania", "French Polynesia": "Oceania", "Christmas Island": "Oceania",
#     "Cocos (Keeling) Islands": "Oceania", "Heard Island and McDonald Islands": "Oceania",

#     # Antarctica
#     "Antarctica (the territory South of 60 deg S)": "Antarctica",
#     "Bouvet Island (Bouvetoya)": "Antarctica",
#     "South Georgia and the South Sandwich Islands": "Antarctica",
#     "French Southern Territories": "Antarctica"
# }

# # was used to add a "Continent" column based on country names
# data["Continent"] = data["Country"].map(lambda x: country_to_continent.get(x, "Unknown"))
# # group by continent
# continent_dic = {continent: group for continent, group in data.groupby("Continent")}

## used to group data by country
# country_dic = {country: group.copy() for country, group in data.groupby("Country")}

# # used to map each continent name to integer to allow graphing
# data["Continent_Code"], _ = pd.factorize(data["Continent"])

# # this block was used to extract date info and split it into separate columns for easier handling
# data["Date"] = pd.to_datetime(data["Date"])
# data["Year"] = data["Date"].dt.year
# data["Month"] = data["Date"].dt.month
# data["Day"] = data["Date"].dt.day


# data.to_csv("modified_climate_change_data.csv", index=False, encoding="utf-8")