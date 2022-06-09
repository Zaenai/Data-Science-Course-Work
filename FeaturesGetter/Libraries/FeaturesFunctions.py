import pandas as pd
import csv
import nltk

import os
import Libraries.cleaning as cleaning
import Libraries.simple_statistics  as statistics

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords

from sklearn.preprocessing import StandardScaler

def preCleanFeatures(data,my_index):
    #Dataframe with content features
    df = pd.DataFrame()
    #Initially set the column to the number of sentences
    df["num_sentences"] = statistics.get_num_sentences(data["content"])
    #print("1")
    df["word_count"]= statistics.preclean_word_count(data["content"])
    #print("2")
    df["avg_sentence_len"] =df["word_count"]/df["num_sentences"] 
    
    df["id"] = data["id"]

    too_short_articles=[["shortID"]]
    to_drop_now=[]
    for (index,num) in zip(df["num_sentences"].index, df["num_sentences"]):
        if(num <3):
            too_short_articles.append([str(data["id"][index])])
            to_drop_now.append(data["id"][index])
    file = open('data/part2'+ str(my_index+1)+'.csv', 'w+', newline ='',encoding='UTF8') 
    with file:     
        write = csv.writer(file)
        write.writerows(too_short_articles)
    old_size = df.shape[0]
    df.drop(axis=0, index= to_drop_now, inplace=True)
    df.filter(["id","avg_sentence_len","num_sentences"]).to_csv(f"data/part{my_index + 1}.csv", encoding='utf-8', index=False)
    print("diff= ",old_size-df.shape[0])

def typeChange(data,my_index):
    def isNonFake(t):
        return 1 if t in ["political", "reliable"] else 0

    def changeTypes(data):
        data["type"] = data["type"].map(isNonFake)

    changeTypes(data)
    data.to_csv('data/part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)

def dropToShortRows(data,my_index):
    def findFstLst(lst,fst,last):
        firstindx=0
        lastindx = 0
        for index,numb in zip(lst.index,lst):
            if (numb >= fst) : 
                firstindx = index 
                break
        for i in range (len(lst)-1,-1,-1):
            if (lst[i] <= last): 
                lastindx = i
                break
        return firstindx,lastindx

    data = data.filter(['id','content','type'])
    data = data.astype({"id":'int32', "content":'object','type' : 'int8'})

    old_rows = data.shape[0]
    toDrop = pd.read_csv("data/tooShort.csv")["shortID"]
    toDrop = toDrop.astype(int)
    toDrop.sort_values()
    print("data indexes: ",data.first_valid_index()," ",data.last_valid_index())
    fst,lst = findFstLst(toDrop,data.first_valid_index(),data.last_valid_index())
    toDrop = toDrop[fst:lst]
    print("rows to drop: ",len(toDrop))
    print("process ",my_index," has indx list")
    for i in toDrop:
        try:
            data.drop(index=i, inplace = True)
        except:
             continue

    data.to_csv(f"data/part{my_index + 1}.csv", encoding='utf-8', index=False)
    print("Difference:", data.shape[0]-old_rows)

def basicClean(data,my_index):
    #cleaning
    cleaning.clean_column(data,"content")
    data.to_csv('data/part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)

def simple_feature(data,my_index):
    makeNanFile = not os.path.isfile('data/part2'+str(my_index+1)+'.csv')
    # print('data/part2'+str(my_index)+'.csv')
    # print(makeNanFile)
    # if(makeNanFile): 
    #     f = open('data/part2'+str(my_index+1)+'.csv', 'w+')
    #     writer = csv.writer(f)
    #     writer.writerow(["nanContent"])

    numb_of_sentences = pd.read_csv(r"features/FeaturesPreClean.csv", skiprows=data.first_valid_index(), skipfooter=data.last_valid_index())
    numb_of_sentences = numb_of_sentences.iloc[:, 1]
    #numb_of_sentences = numb_of_sentences["num_sentences"]
    
    #Dataframe with content features
    df = pd.DataFrame()
    df["id"] = data["id"]
    df["type"] = data["type"]
    df["avg_word_len"], df["lexical_diversity"], df["word_count"], df["vowel_count"], df["min_three_vowels"] = statistics.get_multi_features(data,my_index,makeNan=makeNanFile).T
    #print(df["word_count"])
    
    #Normalizing features
    df["avg_sentence_len"] = df["word_count"]/numb_of_sentences
    df["vowel_count"] = df["vowel_count"]/df["word_count"]
    df["min_three_vowels"] = df["min_three_vowels"]/df["word_count"]
    df.to_csv('data/part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)

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

def speech_parts(data,my_index):#,retDict):
    lemmatizer = WordNetLemmatizer()
    verb_count = []
    noun_count = []
    adjective_count = []
    verbs=0
    nouns=0
    adjectives=0
    #for each article
    for index,article in zip(data["content"].index,data["content"]):
        if(index%100000==0): print("started index ",index)
        #   append results to lists
        lemmatized_article,nouns,verbs,adjectives = lemmatizeNcntSpeech(article,lemmatizer,nouns,verbs,adjectives)
        l = len(lemmatized_article)
        if l == 0: l = 1
        verb_count.append(verbs/l)
        noun_count.append(nouns/l)
        adjective_count.append(adjectives/l)
        #   save lemmatized article in dataFrame 
        data.at[index, "content"]= lemmatized_article
    
    #   save speech-part-ratio data as csv
    print("started saving counts")
    df = pd.DataFrame()
    df["id"] = data["id"]
    df["type"] = data["type"]
    df["verbs_ratio"] = verb_count
    df["noun_ratio"] = noun_count
    df["adjective_ratio"] = adjective_count

    print("started creating csvs speech and lemma")
    df.to_csv('data/part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)
    data.to_csv('data/part2'+str(my_index+1)+'.csv', encoding='utf-8', index=False)

    print("Procces: ",my_index," finished process fun")

def lemmatizeNcntSpeech(article,lemmatizer,n,v,a):
    if(type(article) != str):
        return "",0,0,0
    lemmatized_words=[]
    tokenized_art = word_tokenize(article)
    eng_stopwords = stopwords.words('english')
    #   finds tags (verb,noun etc.)
    tokenized_art_with_tags = nltk.pos_tag(tokenized_art)
    #   for each word
    for i, (word, tag) in enumerate(tokenized_art_with_tags):
        # reject if in stopwords
        if word not in eng_stopwords:
            #   switch to compatible tags
            new_tag = switchTag(tag)
            tokenized_art_with_tags[i] = (word, new_tag)
            #   count speech parts
            if(new_tag==wordnet.NOUN) : n+=1
            elif (new_tag==wordnet.VERB) : v+=1
            elif (new_tag==wordnet.ADJ) : a+=1
            #   lemmatize and concatenate
            lemmatized_words.append(lemmatizer.lemmatize(word,new_tag)+" ")
    return "".join(lemmatized_words),n,v,a

def ConcatanateNTransformFeatures():
    not_importnant = ['lexical_diversity', 'word_count',
                        'min_three_vowels', 'num_sentences',
                'avg_word_lenPost_clean', 'lexical_diversityPost_clean',
                'min_three_vowelsPost_clean', 'adjective_ratio',
                "avg_sentence_len","avg_sentence_lenPost_clean"]

    def transform_data(data):
        id_type = data[["id","type"]]
        data.drop(["id","type"],inplace=True,axis=1)
        data = pd.DataFrame(StandardScaler().fit_transform(data.to_numpy()))
        data = data.round(4)
        data["id"]=id_type["id"]
        data["type"]=id_type["type"]
        return data

    files_lst=["features/FeaturesPreClean.csv","features/FeaturesPostClean.csv","features/Speech_Parts.csv"]
    allFeatures = pd.read_csv("features/FeaturesPostLemmatized.csv")
    allFeatures_cols = allFeatures.columns
    for i in range (3):
        new_csv = pd.read_csv(files_lst[i])
        if "type" in new_csv.columns:
            new_csv.drop(["type"], axis = 1, inplace = True)
        new_csv.drop(["id"], axis=1, inplace = True)
        
        new_csv_cols = new_csv.columns
        for col in new_csv_cols:
            if col in allFeatures_cols :
                allFeatures[col+"Post_clean"]=new_csv[col]
            else: allFeatures[col]=new_csv[col]
        allFeatures_cols = allFeatures.columns
    allFeatures.drop(not_importnant, axis = 1, inplace=True)

    allFeatures =  transform_data(allFeatures)
    allFeatures.to_csv('features/AllFeatures.csv',index=False)


