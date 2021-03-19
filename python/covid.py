# Common Libraries includes packages like
# numpy for linear algebra
# pandas for data processing and file I/O

import numpy as np
import pandas as pd

# urllib for url based access to data
# request.utils for formatting URIs

import urllib.request as url_req
from requests.utils import requote_uri

# plotly.express to view data on the map

import plotly.express as px

# json for processing data in JSON format
# json_normalize : package for flattening json in pandas df

# Json -  libraries for processing Javascript object notation
import json
from pandas import json_normalize

# Geopandas - pandas for mapping
# import geopandas

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# Show data in table format
from tabulate import tabulate

# Additional libraries
from scipy import stats

# Common global functions used across the code base

############## Global Functions Start ################################
# transpose data from a specific column
def transform_data(df=None, name=None):
    return df[df['Country/Region'] == name].iloc[:, 4:].T


# Read data from the url encoded by converting the url to standard format
# ensuring that it is fully and consistently quoted.
#    url   : The url to visit
def read_encoded_data(url=None):
    url_who_table = requote_uri(url)
    with url_req.urlopen(url_who_table) as response:
        data = response.read()
    return data


# Read data in csv format from the url specified
#  url   : The url to visit
#  print : control debug output
def read_csv(url, print=False):
    if len(url) == 0:
        print("URL is missing")
        exit()
    data = pd.read_csv(url)
    if (print):
        data.head()
    return data


############## Global Functions Ends ################################

# Get COVID-19 global data from WHO
global_covid_19_data = read_csv("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")

# Drop the row for global as all others are country specific
is_Global = global_covid_19_data['Name'] != "Global"
global_covid_19_data = global_covid_19_data[is_Global]

print(" The columns in the data are : ", global_covid_19_data.columns)
print(tabulate
      (global_covid_19_data, headers=['Name', 'Region', 'Cases-total',
                                      'Cases_cumulative_total_per_100000',
                                      'Cases_newly_reported_in_last_7days',
                                      'Cases_newly_reported_in_last_7_days_per_100000',
                                      'Cases_newly_reported_in_last_24_hours',
                                      'Deaths_cumulative_total',
                                      'Deaths_cumulative_total_per_100000',
                                      'Deaths_newly_reported_in_last_7days',
                                      'Deaths_newly_reported_in_last_7_days_per_100000',
                                      'Deaths_newly_reported_in_last_24_hours',
                                      'Transmission_Classification'
                                      ]
       )
      )

lat_long_info = pd.read_json("../data/country-codes-lat-long-alpha3.json")
jn = json_normalize(lat_long_info['ref_country_codes'])

# Joining the latitude and longitude information with the country information
ret = global_covid_19_data.join(jn, lsuffix='_caller', rsuffix='_other')
# ret[ret['country']=='Algeria'].latitude

#world_fig = px.choropleth(ret, lat=ret.latitude.astype(int), lon=ret.longitude.astype(int),
#                    color="Cases - cumulative total",
#                    hover_name="Name",
#                    color_continuous_scale=px.colors.sequential.YlOrRd, scope= "world")
#world_fig.show()

#gdf = geopandas.GeoDataFrame(ret, geometry=geopandas.points_from_xy(ret.longitude, ret.latitude))
#world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# World map
#ax = world.plot(color='white', edgecolor='black')

# We can now plot our ``GeoDataFrame``.
#gdf.plot(ax=ax, color='red')
#plt.show()

# NOTE : This is a map that shows details but is not reflected correctly on the map. May need a GeoDataframe. To be tested
world_fig2 = px.scatter_mapbox(data_frame=ret, lat=ret.latitude.astype(int), lon=ret.longitude.astype(int),
                               size=ret["Cases - cumulative total"].astype(int),
                               hover_name='Name', zoom=2,
                               hover_data=['Cases - cumulative total',
                                           'Cases - cumulative total per 100000 population',
                                           'Deaths - cumulative total per 100000 population'
                                           ],
                               mapbox_style='carto-darkmatter', title='Confirmed cases Covid-19 World map.',
                               color_continuous_scale=px.colors.cyclical.IceFire
                               )
world_fig2.show()

# color=ret.,size='Cases - cumulative total per 100000 population'

# Snapshot extracted from John hopkins into data folder
raw_confirmed = pd.read_csv('../data/RAW_global_confirmed_cases.csv')
raw_deaths = pd.read_csv('../data/RAW_global_deaths.csv')
print("The raw data with confirmed :", raw_confirmed.head())

us_conf = pd.read_csv('../data/RAW_us_confirmed_cases.csv')
us_death = pd.read_csv('../data/RAW_us_deaths.csv')
us_meta = pd.read_csv('../data/CONVENIENT_us_metadata.csv')

# Filter 2 data columns - confirmed infection(confirmed) and deaths(deaths) for US for the timeline
us = transform_data(df=raw_confirmed, name='US')
us.columns = ['confirmed']
us['deaths'] = transform_data(df=raw_deaths, name='US').values
print(us.tail())

# Insight 1 : The Aim of this insight is to plot the rise of Covid infection in USA and the associated deaths in US
plt.style.use('seaborn-white')
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 10), gridspec_kw={'height_ratios': [1, 2]})
fig.suptitle('Infections and deaths in USA')
us["confirmed"].plot(y='confirmed', title='Covid-19 spreading in USA', ax=ax1)
us["deaths"].plot(y='deaths', title='Covid-19 deaths in USA', ax=ax2)
plt.show()

ireland = transform_data(df=raw_confirmed, name='Ireland')
ireland.columns = ['confirmed']
ireland['deaths'] = transform_data(df=raw_deaths, name='Ireland').values
print(ireland.tail())

# Insight 2 : The aim of this insight is to provide a visual context on the rise of Covid infections in Ireland
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 10), gridspec_kw={'height_ratios': [1, 2]})
fig.suptitle('Infections and deaths in Ireland')
ireland["confirmed"].plot(y='confirmed', title='Covid-19 spreading in Ireland', ax=ax1)
ireland["deaths"].plot(y='deaths', title='Covid-19 deaths in Ireland', ax=ax2)
plt.show()

# Insight 3:
fig, axes = plt.subplots(2, 2, sharex=True, figsize=(10, 10))

fig.suptitle('Infection and death rates')
axes[0][0].set_title('Ireland Covid Infection')
sns.distplot(x=ireland["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution",
             ax=axes[0][0])
axes[0][1].set_title("Ireland Covid Deaths")
sns.boxplot(ax=axes[0][1], x=ireland["deaths"])

axes[1][0].set_title('US Covid Infection')
sns.distplot(x=us["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution",
             ax=axes[1][0])
axes[1][1].set_title("US Covid Deaths")
sns.boxplot(ax=axes[1][1], x=us["deaths"])

plt.show()
# fig, (ax[1][0], ax[1][0], ax[0][0], ax[0][0]) =plt.subplots(nrows=2, ncols=2, figsize=(18,12))
# plt.subplots_adjust(hspace=0.4, top=0.8)

# Loan amount distribution plots

# sns.distplot(us["confirmed"], fit=stats.gamma, axlabel="Infection rate", label="Infection distribution", ax=ax1[0][0])
# sns.boxplot(us["confirmed"], ax=ax2[0][0])
# plt.show()
# bw_adjust controls the smoothing
# sns.displot(x= tmp.loan_amnt, label="Loan Amount Frequency distribution", kind="kde", bw_adjust=4, ax=ax[0][2])
# sns.displot(x= tmp.loan_amnt, label="Loan Amount Frequency distribution", kind="kde", bw_adjust=0.2, ax=ax[0][3])