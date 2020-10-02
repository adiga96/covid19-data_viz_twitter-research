%load_ext autotime
import datetime
import os, json
import pandas as pd
import numpy as np
import glob
import gzip
from pandas.io.json import json_normalize
import re  
import nltk
pd.set_option('display.max_columns', None)

# Function to extracting dates into a list
# Functions

#1. Data Extractor

def timestamp_extract(month_df):
    try:
        month_df['date'] = [d.date() for d in month_df['created_at']]
    except:
        month_df['date'] = [d.date() for d in month_df['datetime']]
    month_datelist = month_df['date'].astype(str).unique().tolist()
    return month_datelist

#2. State Filteration

def USstate_filteration(f1,K1,K2):
    state_df1 = f1[f1['location'].str.contains(K1, na=False) |  f1['location'].str.contains(K2,case=False, na=False)] 
    state_df1['date'] = [d.date() for d in state_df1['created_at']]
    # datelist = state_merged['date'].astype(str).unique().tolist()
    return state_df1

#3. To calculate @RT Sum and @RT Count

def RT_sum_calculator(date_list, month_df):
    list_sum = []
    for i in date_list:
        screening = month_df[month_df['created_at'].dt.date.astype(str) == i]
        Sum = screening ['retweet_count'].sum()
        list_sum.append(Sum)
    return list_sum

def RT_count_calculator(date_list, month_df):
    list_count = []
    for i in date_list:
        screening = month_df[month_df['created_at'].dt.date.astype(str) == i]
        Count = screening ['retweet_count'].count()
        list_count.append(Count)
    return list_count

#4. Nursing Home Data
#To get the list of values based on True values

def counter(shortage, datelist):
    value = []
    for i in dlist:
        a = len(shortage[shortage['datetime'].dt.date.astype(str) == i])
        value.append(a)

    return value

#5. Code for Normalising Data (Min Max Normalization)

from sklearn import preprocessing
def normaliser(filename):
    
    file_float = filename.values.astype(float)
   # Create a minimum and maximum processor object
    min_max_scaler = preprocessing.MinMaxScaler()

    # Create an object to transform the data to fit minmax processor
    file_scaled = min_max_scaler.fit_transform(file_float)
    

    # Run the normalizer on the dataframe
    file_normalized = pd.DataFrame(file_scaled)
    file_normalized = file_normalized.fillna(0)
    
    file_norm_list = file_normalized.iloc[:,0].tolist()
    
    return file_norm_list 

#6. Plotting Graphs (Tweets vs Hospitalization vs Confirmed Cases)

import matplotlib.pyplot as plt
def plot_graph(datelist,tweets,label1, hosp,label2, cases,label3,med,label4):
    
    plt.plot(datelist,hosp, label = label2)
    plt.plot(datelist,tweets, label = label1)
    plt.plot(cases, label = label3)
    # plt.scatter(datelist, med, marker='o',label = label4)
    plt.plot(datelist, med, '-o', color='red', label = label4)
    plt.xlabel('Date: March-April-May 2020')
    plt.ylabel('Count')
    plt.xticks( rotation='vertical')
    plt.title('Cases vs Tweets :Unique PPE')
    # show a legend on the plot
    plt.legend()
    # Display a figure
    plt.rcParams['figure.figsize']= [20,5]
    
    return plt.show()

#7. Relative Confirmed Cases 

def relative_sum(filename,us_col,col):
    result_sum = filename[col] / filename[us_col]
    return result_sum.tolist()

def relative_count(filename,us_col,col):
    result_count = filename[col] / filename[us_col]
    return result_count.tolist()

#  # READING ALL PPE RELATED DATA
'''
March_All_PPE = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020-03/March_Unique_All_PPE.json', 
							orient = 'records',lines =True) 
April_All_PPE = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020-04/April_Unique_All_PPE.json', 
							orient = 'records',lines =True)
May_All_PPE = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020-05/May_Unique_all_PPE.json',
							orient = 'records',lines =True)
June_All_PPE = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020-06/June_Unique_all_PPE.jsonl',
							orient = 'records',lines =True)
July_All_PPE = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020-07/July_Unique_all_PPE.jsonl', 
							orient = 'records',lines =True)

# To remove RT from full_text to get unique tweets

March_All_PPE = March_All_PPE[~March_All_PPE.full_text.str.contains("RT")]
April_All_PPE = April_All_PPE[~April_All_PPE.full_text.str.contains("RT")]
May_All_PPE = May_All_PPE[~May_All_PPE.full_text.str.contains("RT")]
'''

#Twitter data March to July 2020
twitter_data = pd.read_json('/Users/pritishsadiga/Desktop/Twitter/2020_all/result_twitter_03_07.jsonl', 
							orient = 'records', lines= True)
							
shortage_df = twitter_data[twitter_data['label'] > 0.5 ]
shortage_df = shortage_df.reset_index(drop = True)

# To extract date
'''
march_datelist = timestamp_extract(March_All_PPE)
april_datelist = timestamp_extract(April_All_PPE)
may_datelist = timestamp_extract(May_All_PPE)
# june_datelist = timestamp_extract(June_All_PPE)
# Sum of all date-list March- May
MAM_datelist = march_datelist + april_datelist + may_datelist
'''
# Datelist from March 2020 - July 2020
twitter_data_datelist = timestamp_extract(shortage_df)

# Function 3
ny_twitter = USstate_filteration(shortage_df,'New York', 'NY')
ny_twitter = ny_twitter.reset_index(drop = True)
    
twitter_rtsum = RT_sum_calculator(twitter_data_datelist,shortage_df)
ny_twitter_rtsum = RT_sum_calculator(twitter_data_datelist,ny_twitter)

twitter_rtcount = RT_count_calculator(twitter_data_datelist,shortage_df)
ny_twitter_rtcount = RT_count_calculator(twitter_data_datelist,ny_twitter)

'''
march_RT_sum = RT_sum_calculator(march_datelist, March_All_PPE)
april_RT_sum = RT_sum_calculator(april_datelist, April_All_PPE)
may_RT_sum = RT_sum_calculator(may_datelist, May_All_PPE)
# june_RT_sum = RT_sum_calculator(june_datelist, June_All_PPE)
# sum of all months
us_sum_RT = march_RT_sum + april_RT_sum + may_RT_sum 

march_RT = RT_count_calculator(march_datelist, March_All_PPE)
april_RT = RT_count_calculator(april_datelist, April_All_PPE)
may_RT= RT_count_calculator(may_datelist, May_All_PPE)
# june_RT = RT_count_calculator(june_datelist, June_All_PPE)
# sum of all months
us_count_RT = march_RT + april_RT + may_RT
'''

# No. of COVID 19  Confirmed Cases

cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/Bing-COVID19-Data.csv')
cases['Date'] = pd.to_datetime(cases['Updated'])

US_cases = cases[(cases['Country_Region'] == 'United States') & (cases['AdminRegion1'].isnull())]
US_cases = US_cases[US_cases['Date'].dt.month.between(3,7)]
US_cases_list = US_cases['ConfirmedChange'].tolist()
# US_cases_updated

US_cases_list = US_cases['ConfirmedChange'].tolist()
len(US_cases_list)

# U.S State wise filteration
US_nycases = cases[(cases['Country_Region'] == 'United States') & (cases['AdminRegion1'] == 'New York')
					 & (cases['AdminRegion2'].isnull())]
US_nycases = US_nycases[US_nycases['Date'].dt.month.between(3,7)]

US_nycases = US_nycases.reset_index(drop = True)

ny_cases = US_nycases['ConfirmedChange'].tolist()

# # To read State Confirmed Cases
# NY_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/NY_New_cases.csv')
# # CA_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/CA_New_cases.csv')
# # FL_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/FL_New_cases.csv')
# # WA_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/WA_New_cases.csv')
# # NJ_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/NJ_New_cases.csv')
# # IL_cases = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/Bing_Microsoft_COVID_19/IL_New_cases.csv')
'''
NY_cases_count = NY_cases_count['ConfirmedChange'].tolist()
# CA_cases_count = cases_count(CA_cases)ss
# FL_cases_count = cases_count(FL_cases)
# WA_cases_count = cases_count(WA_cases)
# NJ_cases_count = cases_count(NJ_cases)
# IL_cases_count = cases_count(IL_cases)

'''
# DF to find relative cases
relative_cases_df = pd.DataFrame({'US_cases_count':cases_count,'NY_cases':NY_cases_count,
								'CA_cases':CA_cases_count,'FL_cases':FL_cases_count,
                                'WA_cases':WA_cases_count,'NJ_cases':NJ_cases_count,
                                'IL_cases':IL_cases_count})

NY_relcases = relative_count(relative_cases_df,'US_cases_count','NY_cases')
# CA_relcases = relative_count(relative_cases_df,'US_cases_count','CA_cases')
# FL_relcases = relative_count(relative_cases_df,'US_cases_count','FL_cases')
# WA_relcases = relative_count(relative_cases_df,'US_cases_count','WA_cases')
# NJ_relcases = relative_count(relative_cases_df,'US_cases_count','NJ_cases')
# IL_relcases = relative_count(relative_cases_df,'US_cases_count','IL_cases')

relcases_norm = pd.DataFrame({'NY_relcases':NY_relcases,'CA_relcases':CA_relcases,
								'FL_relcases':FL_relcases,'WA_relcases':WA_relcases,
								'NJ_relcases':NJ_relcases,'IL_relcases':IL_relcases})

NY_cases_norm = normaliser(relcases_norm[['NY_relcases']])
# CA_cases_norm = normaliser(relcases_norm[['CA_relcases']])
# FL_cases_norm = normaliser(relcases_norm[['FL_relcases']])
# IL_cases_norm = normaliser(relcases_norm[['IL_relcases']])
# WA_cases_norm = normaliser(relcases_norm[['WA_relcases']])
# NJ_cases_norm = normaliser(relcases_norm[['NJ_relcases']])

# plt.plot(NY_MAM_datelist,NY_hosp_list, label = "New York: Hospitalized")
plt.plot(NY_MAM_datelist,Rel_NY_cases_count, label = "NY / U.S ")
plt.plot(NY_MAM_datelist,Rel_NJ_cases_count, label = "NJ / U.S ")
plt.plot(NY_MAM_datelist,Rel_WA_cases_count, label = "WA / U.S ")
plt.plot(NY_MAM_datelist,Rel_FL_cases_count, label = "FL / U.S ")
plt.plot(NY_MAM_datelist,Rel_IL_cases_count, label = "IL / U.S ")
plt.plot(NY_MAM_datelist,Rel_CA_cases_count, label = "CA / U.S ")
plt.xlabel('Date: March-April-May')
plt.ylabel('Count')
plt.xticks( rotation='vertical')
plt.title('Relative Cases: Major States')
# show a legend on the plot
plt.legend()
plt.rcParams['figure.figsize']= [20,5]
# Display a figure.
plt.show()


# HOSPITALIZATION DATA


US_hosp['datetime'] = pd.to_datetime(US_hosp['dateChecked'])
US_hosp = US_hosp.reset_index(drop=True)

#filter based on required months (month number)
US_hosp = US_hosp[US_hosp['datetime'].dt.month.between(3,7)]  

US_hosp = US_hosp.reindex(index = US_hosp.index[::-1])    #to reverse the df
US_hosp = US_hosp.reset_index(drop=True)
US_hosp_list = US_hosp['hospitalizedCurrently'].fillna(0).tolist()
nyhosp  = nyhosp.reindex(index = nyhosp.index[::-1]) 
nyhosp = nyhosp.reset_index(drop = True)
nyhosp_1 = nyhosp[['date','hospitalizedCurrently']]

covid_nursing = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/2020_all/COVID-19_Nursing_Home_Dataset.csv')


covid_nursing['datetime'] = pd.to_datetime(covid_nursing['Week Ending'])
covid_nursing = covid_nursing.reset_index(drop=True)

#filter based on required months (month number)
covid_nursing = covid_nursing[covid_nursing['datetime'].dt.month.between(3,7)]  
covid_nursing  = covid_nursing.sort_values(by=['datetime'])
covid_nursing = covid_nursing.reset_index(drop=True)

short = covid_nursing[covid_nursing['Shortage of Aides'] == 'Y']

# Function to extracting dates into a list
def timestamp_extract(month_df):
    month_df['date'] = [d.date() for d in month_df['datetime']]
    month_datelist = month_df['date'].astype(str).unique().tolist()
    return month_datelist

short = short.reset_index(drop= True)

dlist = timestamp_extract(shortage)

def counter(shortage, datelist):
    value = []
    for i in dlist:
        a = len(shortage[shortage['datetime'].dt.date.astype(str) == i])
        value.append(a)

    return value

a = counter(short,dlist)

ny_short = short[short['Provider State'] == 'NY']
ny_short = ny_short.reset_index(drop = True)
b = counter(ny_short,dlist)
# DF = pd.DataFrame({'date':dlist,'medical':a})

DF_ny = pd.DataFrame({'date':dlist,'medical':b})
# creating DF from the Lists above
DF_complete = pd.DataFrame({'date':twitter_data_datelist,'US_sum_RT':twitter_rtsum,
							'US_count_RT':twitter_rtcount,'US_cases':US_cases_list,
							'all_hosp':US_hosp_list})
							
# creating DF from the Lists above
ny_DF_complete = pd.DataFrame({'date':twitter_data_datelist,'US_sum_RT':ny_twitter_rtsum,
								'US_count_RT':ny_twitter_rtcount,'US_cases':ny_cases})	
								
leftjoin_NY = pd.merge(ny_DF_complete,DF_ny, on='date', how='left')
NY_plot_med = pd.merge(leftjoin_NY,nyhosp_1, on='date', how='left')
leftjoin_NY.to_csv('/Users/pritishsadiga/Desktop/leftnyhosp.csv')
nyhosp_1.to_csv('/Users/pritishsadiga/Desktop/nyhosp.csv')
nyhosp_1.to_csv('/Users/pritishsadiga/Desktop/nyhosp.csv')
finallll = pd.read_csv('/Users/pritishsadiga/Desktop/leftnyhosp.csv')

    
    # Normalised Tweets
RTsum_norm = normaliser(leftjoin_med[['US_sum_RT']])
RTcount_norm = normaliser(leftjoin_med[['US_count_RT']])
# Normalised hospital cases
hosp_norm = normaliser(leftjoin_med[['all_hosp']])
# Normalsied Confirmed Cases
cases_norm = normaliser(leftjoin_med[['US_cases']])
med_norm = normaliser(leftjoin_med[['medical']])

# Normalised Tweets
NY_RTsum_norm = normaliser(finallll[['US_sum_RT']])
NY_RTcount_norm = normaliser(finallll[['US_count_RT']])
# Normalised hospital cases
NY_hosp_norm = normaliser(finallll[['hosp']])
# Normalsied Confirmed Cases
NY_ases_norm = normaliser(finallll[['US_cases']])
NY_med_norm = normaliser(finallll[['medical']])

plot_graph(twitter_data_datelist,NY_RTsum_norm,'Shortage NY Tweets',NY_hosp_norm ,
			'Hospitalisation NY', NY_ases_norm,'CasesNY',NY_med_norm,'Reported Shortage NY')
			
import matplotlib.pyplot as plt
def plot_graph(datelist,tweets,label1, hosp,label2, cases,label3,med,label4):
    
    plt.plot(datelist,hosp, label = label2)
    plt.plot(datelist,tweets, label = label1)
    plt.plot(cases, label = label3)
    # plt.scatter(datelist, med, marker='o',label = label4)
    plt.plot(datelist, med, '-o', color='red', label = label4)
    plt.xlabel('Date: March-April-May 2020')
    plt.ylabel('Count')
    plt.xticks( rotation='vertical')
    plt.title('Cases vs Tweets :Unique PPE')
    # show a legend on the plot
    plt.legend()
    # Display a figure
    plt.rcParams['figure.figsize']= [20,5]
    
    return plt.show()
    
plot_graph(twitter_data_datelist,RTcount_norm,'Shortage Tweets',hosp_norm ,'Hospitalisation',
			cases_norm,'Cases',v,'Reported Shortage')
