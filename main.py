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

#2. COVID TRACKING PROJECT- DATA

# API request
import requests
url1 = 'https://api.covidtracking.com/v1/us/daily.json'
url2 = 'https://api.covidtracking.com/v1/states/daily.json'
r1 = requests.get(url1)
r2 = requests.get(url2)
data_dict_1 = r1.json()
data_dict_2 = r2.json()

Covid_DF = pd.DataFrame.from_dict(data_dict_1)
Covid_states_DF = pd.DataFrame.from_dict(data_dict_2)
# Covid_states_DF

# statehosp = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/2020_all/all-states-history (1).csv')

def state_extractor_COVTP(dataframe,state,mon_start,mon_end):
    
    df = dataframe[dataframe['state'] == state]
    df = df.reset_index(drop= True)

    # Since the data doesn't have a timestamp, we need to convert the string dates to Timestamp

    initial_datelist = df['date'].tolist()

    initial_date_df = pd.DataFrame(data=list(enumerate(initial_datelist, start=1)), columns=['id','int_date'])
    # converting to timestamp
    initial_date_df[['str_date']] = initial_date_df[['int_date']].applymap(str).applymap(lambda s: "{}-{}-{}".format(s[0:4],s[4:6],s[6:]))
    df['datetime'] = pd.to_datetime(initial_date_df['str_date'])
    # df['datetime'] = pd.to_datetime(df['date'])
    df['date'] = [d.date() for d in df['datetime']]

    df = df[df['datetime'].dt.month.between(mon_start,mon_end)]  #filter based on required months (month number)
    df = df.reindex(index = df.index[::-1])    #to reverse the df
    df = df.reset_index(drop=True)
    df_reduced = df[['date','state','positive','negative','totalTestResults','positiveIncrease','negativeIncrease','total','hospitalizedCurrently', 
                    'hospitalizedCumulative','hospitalizedIncrease','onVentilatorCurrently','onVentilatorCumulative','recovered','death',
                    'deathConfirmed','deathProbable','deathIncrease','datetime']]
    
    return df_reduced

# Month Wise
New_York = state_extractor_COVTP(Covid_states_DF,'NY',3,9)
# California = state_extractor_COVTP(Covid_states_DF,'CA',3,8)
# Texas = state_extractor_COVTP(Covid_states_DF,'TX',3,8)

# Recovered Cases (since -ve value found in data)
recovered = New_York[['date','recovered']]
recovered['recoveredIncrease'] =  recovered['recovered'].diff()
recovered[recovered['recoveredIncrease'] < 0] = 0
s = pd.concat([New_York,recovered['recoveredIncrease']], axis = 1)
New_York = s

New_York_Viz = New_York[['date','datetime','state','positiveIncrease','hospitalizedCurrently','onVentilatorCurrently','recoveredIncrease','deathIncrease']]
# California_Viz = California[['date','datetime','state','positiveIncrease','hospitalizedCurrently','onVentilatorCurrently','recoveredIncrease','deathIncrease']]

#Normalising Data
New_York_Viz_cases_Norm = normaliser(New_York_Viz[['positiveIncrease']])
New_York_Viz_hosp_Norm = normaliser(New_York_Viz[['hospitalizedCurrently']])
New_York_Viz_critical_Norm = normaliser(New_York_Viz[['onVentilatorCurrently']])
New_York_Viz_recovered_Norm = normaliser(New_York_Viz[['recoveredIncrease']])
New_York_Viz_death_Norm = normaliser(New_York_Viz[['deathIncrease']])

# Plot all COVID 19 data
plt.plot(New_York_Viz['date'],New_York_Viz_cases_Norm,color='red')
plt.plot(New_York_Viz['date'],New_York_Viz_hosp_Norm,color='blue')
plt.plot(New_York_Viz['date'],New_York_Viz_critical_Norm,color='green')
plt.plot(New_York_Viz['date'],New_York_Viz_recovered_Norm,color='brown')
plt.plot(New_York_Viz['date'],New_York_Viz_death_Norm,color='black')
plt.rcParams['figure.figsize']= [20,5]


#3. Nursing Homes and Medical Center Data
covid_nursing = pd.read_csv('/Users/pritishsadiga/Desktop/Twitter/2020_all/COVID-19_Nursing_Home_Dataset.csv')


covid_nursing['datetime'] = pd.to_datetime(covid_nursing['Week Ending'])
covid_nursing = covid_nursing.reset_index(drop=True)
covid_nursing = covid_nursing[covid_nursing['datetime'].dt.month.between(3,8)]  #filter based on required months (month number)
covid_nursing  = covid_nursing.sort_values(by=['datetime'])
covid_nursing = covid_nursing.reset_index(drop=True)

short = covid_nursing[covid_nursing['Shortage of Aides'] == 'Y']
short = short.reset_index(drop= True)

# Extract weekend dates from May 2020
dlist = timestamp_extract(short)

# Function 4
usa_shortage = counter(short,dlist)
# len(dlist)
covid_nursing.columns.tolist()
usa_shortage = counter(short,dlist)
usa_shortage

ny = short[short['Provider State'] == 'NY' ]
ny = ny.reset_index(drop = True)
ny_shortage = counter(ny,dlist)

#Define a Function for ALL Nursing Home Shortage Data
'''
ca = short[short['Provider State'] == 'CA' ]
ca = ca.reset_index(drop = True)
ca_shortage = counter(ca,dlist)
# ny_shortage

ny_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':ny_shortage})
ca_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':ca_shortage})
fl_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':fl_shortage})
tx_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':tx_shortage})
az_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':az_shortage})
wa_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':wa_shortage})
nj_DF_complete = pd.DataFrame({'Date':dlist,'Shortage':nj_shortage})

def short_plot(shortagelist,hosplist,dlist,label):

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12]
    # grades = ['F', 'D', 'C', 'B', 'A'] DATElist
    plt.title(f"{label}")
    plt.xlabel("Date")
    plt.ylabel("Count")

    # plt.bar(x, ny_shortage, color = "orange", edgecolor = 'black', linewidth = 1)
    plt.plot(x, shortagelist, '-o',color='red', label = 'Shortage reported')
    plt.plot(dlist, hosplist, '-o', color = 'blue', label = 'Total Hospitalizations')
    plt.xticks(x,dlist)

    # Bar Charts with Values in Center
    '''
    xlocs, _ = plt.xticks()
    i = 0
    for j in shortagelist:
        plt.text(xlocs[i] - 0.1, j + 2, str(j))
        i += 1
    '''
    plt.legend()
    plt.rcParams['figure.figsize']= [20,5]
    return plt.show()
