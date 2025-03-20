# Climate_MachineLearning

## This is the repo for our machine learning project on climate change data.

### Original datasets:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change

### Summary:
    So far, I have modified the sea_ice dataset to fit the structure of the ave_temp_change data set, i.e. i
    converted the daily measurements from both the Norther and Southern Hemispheres, into monnthly averages. 
    Then I added each of these monthly averages pairwise (the ones matching by year and month) to get the global
    monthly average for every month reaching back to 1978

    The ave_temp_change is pretty untouched so far. The next step would be to gather other intereseting datasets,
    such as the monthly average of global CO 2 in earth atmosphere, as well as the total amount of forest per month.