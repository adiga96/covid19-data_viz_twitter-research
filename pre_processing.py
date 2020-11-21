%load_ext autotime
import datetime
import os, json
import pandas as pd
import numpy as np
import glob
import gzip
from pandas.io.json import json_normalize
pd.set_option('display.max_columns', None)

# To check for folder containing tweets
for folder in glob.glob('/Volumes/My Passport/MS_Thesis/COVID_Tweets/2020-10/*'):
    print(f'NEW FOLDER-------------------{folder}')     
        # To check for .jsonl.gz file inside the folder
    for f in glob.glob(f'{folder}/*.jsonl.gz'):
            try:
                print(f'{f} New File ____________________________________________')
            
                #reading the json file
                read_json = pd.read_json(f, orient='records', lines=True, chunksize = 10000)
                for chunk in read_json:
                    
                    #Data_Sorting
                    tweet_objects = chunk                     
                    normalize_tweet_user = pd.json_normalize(chunk['user'])
                    user_location = normalize_tweet_user[['location','geo_enabled']]
                    tweets_df = pd.concat([tweet_objects,user_location], axis=1)
                    tweets_df = tweets_df.drop_duplicates('id')
                    tweets_df.replace('', np.nan, inplace=True)
                    tweets_df = tweets_df[tweets_df['location'].notna()]
                    
                    #filtering to US_locations only # Check for location_filteration.py
                    print('filtering via US_location')
                    Tweets_US_location = tweets_df[tweets_df['location'].isin(city_state_list) | tweets_df['location'].isin(city_stateid_list) | 
                                                    tweets_df['location'].isin(city_county_list) | tweets_df['location'].isin(US_list) |
                                                    tweets_df['location'].isin(state_id_unique_list) |  tweets_df['location'].isin(state_unique_list)|
                                                    tweets_df['location'].isin(only_city) | tweets_df['location'].isin(city_country_list)| 
                                                    tweets_df['location'].isin(city_country1_list) |tweets_df ['location'].isin(state_country_list)|
                                                    tweets_df['location'].isin(state_country1_list)]

                    
                    #sorting and filtering shortage of essential medical products
                    print('filtering based on Keywords') 
                    # checking for tweets with all_PPE
                    All_PPE = Tweets_US_location [Tweets_US_location ['full_text'].str.contains(r'\b(ppe|mask|shortage|N95|medical supplies|surgical|ventilator|respirator|ICU|glove|#ppe|wipes|sanitizer|                                                                                                        disinfectant| protective equipment|#WearAMask|#GetUsPPE|#MaskUp|#HelpUsHelpYou|#PPE|#ppenow)\b', case=False, na=False) ]  
                    All_PPE = All_PPE.drop_duplicates('full_text')   
                    

                    
                    #Processing Tweets   
                    #removing punctuations
                    All_PPE ['text_processed'] = All_PPE ['full_text'].apply(lambda x: remove_punct(x))
                    print('text_processed')

                    # Tokenization
                    All_PPE ['text_tokenized'] = All_PPE ['text_processed'].apply(lambda x: tokenization(x.lower()))
                    print('text_processed')
                    
                    # Removing Stopwords  - English, Spanish, Italian, German, French
                    All_PPE['text_nostopwords'] = All_PPE['text_tokenized'].apply(lambda x: remove_stopwords(x))
                    print('stop words removed')

                    # Stemming 
                    All_PPE['text_stemmed'] = All_PPE['text_nostopwords'].apply(lambda x: stemming(x))
                    print('stemmed')
                    
                    # Lemmatization
                    All_PPE['text_lemmatized'] = All_PPE['text_stemmed'].apply(lambda x: lemmatizer(x))
                    print('lemmitized')
                
                    #total count of all the shortages
                    
                    out = All_PPE.to_json(orient='records', lines= True, compression ='gzip')
                    out += '\n'
                    out = out.encode('utf-8')
                    with open('/Users/pritishsadiga/Desktop/Twitter/2020-10/October_PPE.jsonl', 'ab') as f:
                        f.write(out)
                        print('File Saved______________________________________________')
            except e:
                with open('/Users/pritishsadiga/Desktop/Twitter/2020-10/October_errors.txt', 'a') as e:
                    e.write(f'{f}')
