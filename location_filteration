%load_ext autotime
import json
import pandas as pd
import numpy as np

# Code for creating US_location_df

USA = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/US_city_list.csv')
# USA = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/NY_location.csv')
USA['city_state'] = USA['city_ascii'].str.cat(USA['state_name'], sep =", ")
USA['city_stateid '] = USA['city_ascii'].str.cat(USA['state_id'], sep =", ")
USA['city_county'] = USA['city_ascii'].str.cat(USA['county_name_all'], sep =", ")
USA['city_country'] = USA['city_ascii'].str.cat(USA['Country'], sep =", ")
USA['city_country1'] = USA['city_ascii'].str.cat(USA['Country_1'], sep =", ")
USA['state_country'] = USA['state_name'].str.cat(USA['Country'], sep =", ")
USA['state_country1'] = USA['state_name'].str.cat(USA['Country_1'], sep =", ")
USA.to_csv('/Users/pritishsadiga/Desktop/Twitter/US_location_df.csv')

# List of USA_locations
city_state_list = USA['city_state'].tolist()
city_stateid_list = USA['city_stateid'].tolist()
city_county_list = USA['city_county'].tolist()
city_country_list = USA['city_country'].tolist()
city_country1_list = USA['city_country1'].tolist()
state_country_list = USA['state_country'].tolist()
state_country1_list = USA['state_country1'].tolist()
US_list = ['USA','US', 'United States','United States of America']

# creating list of all unique states/state id's (total = 52) in the US
state_id_unique_list = (USA['state_id'].unique()).tolist()
state_unique_list = (USA['state_name'].unique()).tolist()
only_city = (USA['city_ascii'].unique()).tolist()

# To filter tweets via location----
'''
NY_boroughs_list = ['New York','Manhattan','Kings', 'Brooklyn', 'Bronx', 'Queens', 'Staten Island','Richmond', ]
tweets_nyc = USA[USA['county_name_all'].isin(NY_boroughs_list)]
city_state_list = tweets_nyc['city_state'].tolist()
city_stateid_list = tweets_nyc['city_stateid'].tolist()
city_county_list = tweets_nyc['city_county'].tolist()
city_country_list = tweets_nyc['city_country'].tolist()
city_country1_list = tweets_nyc['city_country1'].tolist()
