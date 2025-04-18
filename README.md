# Climate_MachineLearning

## This is the repo for the machine learning project of group KAPPA on climate change data.

### Original datasets:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change
    co2 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv
    co2 annual mean:https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv
    co2 annual growth:https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.csv
    ch4 monthly mean:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv
    ch4 annual mean:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv
    ch4 annual growth:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_gr_gl.csv 

### Description:

    The idea is to essentially gather two types of data sets: growthrate, and absolute value. For each of the features we are considering (Temperature, Sea Ice, CO2, CH4 so far) we want to acquire the data both as a monthly and as an annual version, to allow for in depth analysis and detection of trends and patterns both longterm and seasonal.

    We are currently in the first phases of solving the task of successfully predicting climate trends. Right now we are focussing on temperature prediction based on the annual dataset. We plan on expanding and refining our approach using the monthly dataset as well. Additionally, we intent to fill in the missing data for the most recent years (hopefully we will have complete data until 2024), as well as engineering / adding more features. For example the categorical feature of 'Hemisphere' for each country, which might allow some interesting classification approaches to try and train models which can successfully predict the hemisphere a country is located in based on the data it is given. 

### Contents:

    FILES INCLUDED: 
        - data
            |--- annual
                |--- annual_data_trim.csv
                |--- annual_data.csv
            |--- monthly
                |--- monthly_data_trim.csv
                |--- monthly_data.csv
            |--- original
                |--- NOAA
                    |--- ORIGINAL DATASETS
                |--- ave_temp_change.csv
                |--- readme.txt
                |--- sea_ice.csv
            |--- preprocessed

        - eda
            |--- EDA_annual.py
            |--- EDA_monthly.py
            |--- edaScript.py
        
        - models
            |--- plots
                |--- PLOTS OF MODEL RUNS
            |--- forest_climate.py
            |--- linear_regression_climate.py
        
        - visualizations
            |--- annual
                |--- ANNUAL DATA EDA VISUALIZATIONS
            |--- monthly
                |--- MONTHLY DATA EDA VISUALIZATIONS
        
        - AnnualDataSetCreation.py
        - MonthlyDataSetCreation.py
        - PrepareAveTempSet.py
        - PrepareSeaIceSet.py
        - README.md
        - requirements.txt

### SYSTEM REQUIREMENTS:

    - Python 3.10.x (3.10 or higher)
### Usage:    

    Extract this directory into a directory of your choice where you would like to work with this
    project in. Then open a terminal session and navigate to that directory and execute the following
    commands:

    ```console
    pip install virtualenv
    python -m venv venv
    pip install -r requirements.txt
    ```
    Now you are ready to run any .py script contained in this directory structure. By doing the following:
    Navigate to the directory in your terminal session where the script you want to run is located in.
    Then execute a command of the following structure:

    ```console
    python <The_Script>.py
    ```
