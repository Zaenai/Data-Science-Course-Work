
import imp
import pandas as pd
import time

from pyparsing import rest_of_line
import Libraries.simple_statistics
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.cleaning
import Libraries.simple_statistics
import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('corpus')
# nltk.download('all')
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from cleantext.sklearn import CleanTransformer # likely required to ´pip install clean-text´
import multiprocessing

#changes tags and count them
def switchTag(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif (tag.startswith('J') or
            tag.startswith('A')):
        return wordnet.ADJ
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN 


# gets a chunk of data, cleans it and saves as 
def process_function(data,my_index,retDict):
    #data=Data.copy(deep=True)
    lemmatizer = WordNetLemmatizer()
    df = pd.DataFrame()
    verb_count = []
    noun_count = []
    adjective_count = []
    eng_stopwords = stopwords.words('english')
    for index,article in zip(data["content"].index,data["content"]):
        verbs=0
        nouns=0
        adjectives=0
        lemmatized_article=""
        tokenized_art = word_tokenize(article)
        tokenized_art_with_tags = nltk.pos_tag(tokenized_art)
        for i, (word, tag) in enumerate(tokenized_art_with_tags):
            if word not in eng_stopwords:
                new_tag = switchTag(tag)
                if(new_tag==wordnet.NOUN) : nouns+=1
                elif (new_tag==wordnet.VERB) : verbs+=1
                elif (new_tag==wordnet.ADJ) : adjectives+=1
                tokenized_art_with_tags[i] = (word, new_tag)
                lemmatized_word = lemmatizer.lemmatize(word,new_tag)+" "
                lemmatized_article+=lemmatized_word
        verb_count.append(verbs/len(lemmatized_article))
        noun_count.append(nouns/len(lemmatized_article))
        adjective_count.append(adjectives/len(lemmatized_article))
        data.at[index, "content"]= lemmatized_article
        
    df["verbs_ratio"] = verb_count
    df["noun_ratio"] = noun_count
    df["adjective_ratio"] = adjective_count
    df.to_csv('data/ver_noun_adj'+str(my_index+1)+'.csv', encoding='utf-8', index=False)
    retDict[my_index] = data

def get_text_distribution(data, col):
    fake_text = []
    true_text = []
    true = data.loc[data['type'] == 1]#true
    fake = data.loc[data['type'] == 0]#fake
    for text in fake[col]:
        #print(text.split(" "))
        fake_text += text.split(" ")
    for text in true[col]:
        #print(text.split(" "))
        true_text += text.split(" ")
    return (FreqDist(fake_text),FreqDist(true_text))


def main():
    numberOfProc = 1
    manager = multiprocessing.Manager()
    ret_dict = manager.dict()
    #   Read data, drop usless ONLY content, title and type left!
    data = pd.read_csv(r"data/NewTypesCleanedMilion.csv" ,nrows = 1000)

    process_list = []
    
    for i in range(numberOfProc):
        p = multiprocessing.Process(target=process_function, args=(data, i, ret_dict))
        process_list.append(p)
    
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

    new_data= pd.DataFrame()
    for i in range(numberOfProc):
        new_data = pd.concat([new_data,ret_dict[i]],ignore_index=True)
    
    
    print(new_data.shape)
    print(new_data["content"][0])
    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/ver_noun_adjX","data/speech_parts")

    distr_tuple = get_text_distribution(new_data,"content")
    print("FAKE: ",distr_tuple[0].most_common(15))
    print("TRUE: ",distr_tuple[1].most_common(15))

if __name__ == '__main__':
    main()

