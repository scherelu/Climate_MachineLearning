"""
This file is used to manipulate all of our datasets and to merge them into a comprehenseive one.
The annual data set is already merged, the monthly dataset is still work in progress. Sadly I realized too late
that we need to hand this in aswell. While I do have a record of how I manipulated the datafiles, I did not have
time to reconstruct all of the python code that went into it. The methods how we attained our final datasets
will of course be included in our final report for transparency.

Original Datasets:

    sea_ice: https://www.kaggle.com/datasets/nsidcorg/daily-sea-ice-extent-data
    ave_temp_change: https://www.kaggle.com/datasets/sevgisarac/temperature-change
    co2 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv
    co2 annual mean: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.csv
    co2 annual growth: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_gr_gl.csv
    ch4 monthly mean: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv
    ch4 annual mean: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_annmean_gl.csv
    ch4 annual growth: https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_gr_gl.csv

NOTE: 
    The missing data between 1961 and 1979 in the co2 annual mean dataset was manually completed using  
    https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt 
    
    The missing data betwen 1961 and 1984 in the ch4 annual mean dataset was manually completed using
    https://sealevel.info/co2_and_ch4.html ; Since the recorded values are only biyearly, interpolation 
    was used.

"""