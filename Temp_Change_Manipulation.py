import pandas as pd

data = pd.read_csv("maybe/annual_temp_change.csv")

months = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

seasons = ["Dec?Jan?Feb","Mar?Apr?May","Jun?Jul?Aug", "Sep?Oct?Nov"]

# data["Temp_Change_C"] = data["Value"]
data = data[["Country","Year","Temp_Change_C"]]

data.to_csv("maybe/annual_temp_change.csv", index=False)

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