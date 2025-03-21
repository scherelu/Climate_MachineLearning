import pandas as pd

data = pd.read_csv("data/annual/co2_gr_gl.csv", header=43)

# months = ["January", "February", "March", "April", "May", "June", "July", "August",
#           "September", "October", "November", "December"]

# seasons = ["Dec?Jan?Feb","Mar?Apr?May","Jun?Jul?Aug", "Sep?Oct?Nov"]

data = data[["year","ann inc"]]

data.to_csv("data/annual/co2_gr_gl.csv", index=False)

# data["Temp_Change_C"] = data["Value"]

## --------------------------------------------------------------------------
### This block was to remove countries that were missing entry years, such as Yugoslavia, USSR, Sudan, etc.
# # croup by country and check completeness
# incomplete_countries = []

# expected_years = set(range(1961,2021))

# for country, group in data.groupby("Country"):
#     years_present = set(group["Year"])
#     if years_present != expected_years:
#         missing_years = sorted(expected_years - years_present)
#         incomplete_countries.append((country, len(missing_years), missing_years))

# # create a DataFrame of incomplete countries
# incomplete_df = pd.DataFrame(incomplete_countries, columns=["Country", "Missing_Count", "Missing_Years"])

# complete_countries = set(data["Country"].unique()) - set(incomplete_df["Country"])
# clean_data = data[data["Country"].isin(complete_countries)]

# clean_data.to_csv("cleaned_annual_temp.csv", index=False)
##-----------------------------------------------------------

# ## Split the total dataset into smaller pieces for easier and faster processing
# # Define country groups (adjust ranges as needed)
# country_groups = {
#     "A-B": ["A", "B"],
#     "C-F": ["C", "D", "E", "F"],
#     "G-K": ["G", "H", "I", "J", "K"],
#     "L-O": ["L", "M", "N", "O"],
#     "P-S": ["P", "Q", "R", "S"],
#     "T-Z": ["T", "U", "V", "W", "X", "Y", "Z"]
# }

# # Loop through groups and save separate CSV files
# for group, letters in country_groups.items():
#     subset = data[data["Area"].str[0].isin(letters)]
#     subset.to_csv(f"_{group}_temperature.csv", index=False)
#     print(f"Saved: _{group}_temperature.csv ({len(subset)} rows)")