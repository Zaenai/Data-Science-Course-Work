# psh270, jxs535, fgp424, hkp680

import nltk as nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('corpus')
#nltk.download('all')
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from cleantext.sklearn import CleanTransformer # likely required to ´pip install clean-text´
from cleantext import clean
import time
#data = pd.read_csv("https://raw.githubusercontent.com/several27/FakeNewsCorpus/master/news_sample.csv")
data = pd.read_csv(r"C:\Users\Computer\Documents\GitHub\Data-Science-Course-Work\CSVs\1mio-raw.csv", nrows = 1000)

def drop_useless_data(data):
    #Dropping unneeded columns
    cols_to_delete = ["Unnamed: 0","id","scraped_at","inserted_at","updated_at"]
    for column in data.columns:
        if data[column].isnull().values.all():
            cols_to_delete.append(column)
    data.drop(cols_to_delete, 1, inplace=True)
    
    #Dropping entries with nan type
    data.dropna(subset = ["type"], inplace = True)
    #Dropping entries with unknown type
    data.drop(data.loc[data["type"] == "unknown"].index, inplace=True)
    not_enough_of_type = ["clickbait", "reliable", "unreliable", "bias", "hate", "junksci"]
    for t in not_enough_of_type:
        data.drop(data.loc[data["type"] == t].index, inplace=True)

#drop_useless_data(data)
print("data size after initial  drop:", data.shape[0])
# hree_numb_date = r'(<number> <number> <number>)' #YYYY/MM/DD or DD/MM/YYYY or MM/DD/YYYY
# literal_months_date= r'(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\S* ((<number> ){1,2}|([0-9]{1,2}(st|nd|rd|th)))' #Eg. jun 2nd 2020, january 23. 2021
# literal_months_reverse_date = r'((number {1,2})|[0-9]{1,2}(st|nd|rd|th)) *(jan|feb|mar|apr|may|jun|jul|aug|sep|nov|dec)\S*' #Eg. 10th february, 4th july
# all_dates = (three_numb_date) +'|' + (literal_months_date) +'|'+ (literal_months_reverse_date)
# multiple_chars = r'(.)\1{3,}'
# special_symbols = r'([^<>a-z ])'#Matches special symbols such as © or ™
# single_letter = r' [a-z] ' #matches single letters

initial_cleaner = CleanTransformer(fix_unicode=True,               # fix various unicode errors
                                    to_ascii=True,                  # transliterate to closest ASCII representation
                                    lower=True,                     # lowercase text
                                    no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
                                    no_urls=True,                  # replace all URLs with a special token
                                    no_emails=True,                # replace all email addresses with a special token
                                    no_phone_numbers=True,         # replace all phone numbers with a special token
                                    no_numbers=True,               # replace all numbers with a special token
                                    no_digits=True,                # replace all digits with a special token
                                    no_currency_symbols=True,      # replace all currency symbols with a special token
                                    no_punct=True,                 # remove punctuations
                                    lang="en"                       # set to 'de' for German special handling
                                    )

def clean_column(data, col_name):
    for i, entry in zip(data[col_name].index, data[col_name]):    
        #We first convert to lower case and replace punctuation with space such that dates can
        #more easily be processed (eg. 10.12.2020 -> 10 12 2020 -> <NUMBER> <NUMBER> <NUMBER> instead of <NUMBER><NUMBER><DIGIT> or something)
        cleaned = initial_cleaner.transform([entry])[0]
        #cleaned = re.sub(special_symbols,'',cleaned)
        #cleaned = re.sub(multiple_chars, '', cleaned)
        #cleaned = re.sub(single_letter, '',cleaned)
        data.at[i, col_name] = cleaned

def clean_data(data):
    
    start_time = time.time()
    clean_column(data, "content")
    stop_time = time.time()
    content_clean_time = stop_time - start_time
    
    start_time = time.time()
    clean_column(data, "title")
    stop_time = time.time()

    title_clean_time = stop_time - start_time

    print(f"content = {content_clean_time}, title: {title_clean_time}") 


clean_data(data)


# 0,00875 
# 8.750

# time per article 1.75/200 = 0,00875
# 0,00875 * 1E6 = 8750
#8750/60 = 145





