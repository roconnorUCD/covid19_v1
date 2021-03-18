# Check option to build maps using folium or leaflet

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

# Packages for interaction with web requests. Get data from web server
import urllib.request as url_req
from requests.utils import requote_uri

# Visualization libraries0
import matplotlib.pyplot as plt
import seaborn as sns

############## Global Functions ################################
# transpose data from a specific column
# def transpose_data(df=None, name=None, colNum =0 ):
#    return df[df['Country/Region'] == name].iloc[:, colNum:].T

def transform_data(df=None, name=None):
    return df[df['Country/Region'] == name].iloc[:, 4:].T


# Read data from the url encoded
def read_encoded_data(url=None):
    url_who_table = requote_uri(url)
    with url_req.urlopen(url_who_table) as response:
        data = response.read()
    return data


# Read data in csv format from the url specified
def read_csv(url, print=False):
    if len(url) == 0: print("URL is missing")

    data = pd.read_csv(url)
    if (print):
        data.head()
    return data

############## Global Functions Ends ################################

# get covid-19 global data
global_covid_19_data = read_csv("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")
print(" The columns in the data are : ", global_covid_19_data.columns)

# Snapshot extracted from John hopkins into data folder :
raw_confirmed = pd.read_csv('./data/RAW_global_confirmed_cases.csv')
raw_deaths = pd.read_csv('./data/RAW_global_deaths.csv')

print("The raw data with confirmed :", raw_confirmed.head())

# Transpose data from colnum 4 onwards
us = transform_data(df=raw_confirmed, name='US')
print(us.head(5))

us_conf = pd.read_csv('./data/RAW_us_confirmed_cases.csv')
us_death = pd.read_csv('./data/RAW_us_deaths.csv')
us_meta = pd.read_csv('./data/CONVENIENT_us_metadata.csv')

us = transform_data(df=raw_confirmed, name='US')
us.columns = ['confirmed']
us['deaths'] = transform_data(df=raw_deaths, name='US').values
us.tail()

us_map = us.plot(y='confirmed', title='USA Covid-19 spreading')
#us = us.na.fill("None")
us_map.show()
