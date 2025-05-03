# Climate_MachineLearning

## This is the repo for the machine learning project of group KAPPA on climate change data.

### Original datasets:

    ALL SEA ICE DATASETS: https://noaadata.apps.nsidc.org/NOAA/G02135/
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change
    co2 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv
    co2 annual mean:https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv
    co2 annual growth:https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.csv
    ch4 monthly mean:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv
    ch4 annual mean:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv
    ch4 annual growth:https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_gr_gl.csv 

### Description:

    The idea is to essentially gather two types of data: growthrate, and absolute value. For each of the features we are considering (Temperature, Sea Ice, CO2, CH4) we want to acquire the data both as a monthly and as an annual version, to allow for in depth analysis and detection of trends and patterns both longterm and seasonal.

    As mentioned, the aim of the scripts in this codebase is to uncover trends and connections within our
    datasets. We targeted both the 'hemisphere' feature with the VotingClassifier.py script, and the temp_change_c feature using the VotingRegressor_Temp_Ann.py script. Another interesting analysis was
    conducted using the VotingRegressor_Temp_Mon.py script, where we configured the model to predict the
    evolution of a countries' temperature change individually, and then rank the countries based on these
    predictions into a top and bottom 10.

    If you want to reconstruct the datasets, you need to run the following scripts in this order:
        1. PrepareAveTempSet.py
        2. PrepareSeaIceSet.py
        3. MonthlyDataSetCreation.py
        4. AnnualDataSetCreation.py

    This is because some scripts depend on datasets created by one of the others. However, all datasets are already created and in the 'data' directory. So there shouldn't be any issues regarding this.

    Note that the primary datasets chosen for anlysis, were the 'annual_data_trim.csv' inside 'data/annual/',
    and the 'monthly_data_trim.csv' located under 'data/monthly/', as both of them do not have any missing
    data entries. That way we have a complete dataset covering the period from 1979 until 2020 (inclusive),
    both for monthly and annual data. 

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
            |--- optimizing
                |--- SCRIPTS USED FOR HYPERPARAMETER TUNING
            |--- plots
                |--- PLOTS OF MODEL RUNS
            |--- forest_climate.py
            |--- linear_regression_climate.py
            |--- randomF.py
            |--- VotingClassifier_Hem.py
            |--- VotingRegressor_Temp_Ann.py
            |--- VotingRegressor_Temp_Mon.py
            |--- xboost.py
        
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
