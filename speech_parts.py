
import pandas as pd
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import pandas as pd
import time
import os
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('corpus')
# nltk.download('all')

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


# finds verbs,nouns and adjectives ratio, also
# returns dataframe with lemmatized content column
def process_function(data,my_index,retDict):
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
    df["verbs_ratio"] = verb_count
    df["noun_ratio"] = noun_count
    df["adjective_ratio"] = adjective_count

    print("started creating csvs speech and lemma")
    df.to_csv('data/ver_noun_adj'+str(my_index+1)+'.csv', encoding='utf-8', index=False)
    data.to_csv('data/lemmatized'+str(my_index+1)+'.csv', encoding='utf-8', index=False)
    
    # returns data with lemmatized content
    print("saving return")
    retDict[my_index] = data
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


def print_text_distribution(data, col,type,numb_of_common):
    type_int = 0 #fake
    if (type=="true"): type_int = 1 #true
    text = []
    data_of_type = data.loc[data['type'] == type_int]
    for art_content in data_of_type[col]:
        text += art_content.split(" ")
    print(type,": ",FreqDist(text).most_common(numb_of_common))

 

def main():
    # 45min for milion 

    start_time = time.time()
    #   specify number of processes
    numberOfProc = 8
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of csv to read from
    csv_to_read_name = "NewTypesCleaned"
    #   specify names of new csv file with cleaned data
    new_speach_parts_file_name = "Speech_Parts"
    new_lemmatized_file_name = "Lemmatized"

    #   read cleaned data with new types 
    data = pd.read_csv("data/"+csv_to_read_name+".csv" ,nrows=rows)

    # use multiprocessing to create speech parts ratio csv,
    # and return lemmatized data
    tuple = proces.make_processes_with_return(data, numberOfProc, process_function)
    process_list = tuple[0]
    return_Dictionary = tuple[1]
    print(proces.run_proc(process_list))
    lemmatized_data= pd.DataFrame()

    print("started concatanate lemmatized data")
    for i in range(numberOfProc):
        lemmatized_data = pd.concat([lemmatized_data,return_Dictionary[i]],ignore_index=True)
    
    print("started concatanate speech-part files ")
    # concatanate speech-part csv files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/ver_noun_adjX","data/"+new_speach_parts_file_name)

    print("started concatanate lematized files ")
    # concatanate lemmatized csv files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/lemmatizedX","data/"+new_lemmatized_file_name)

    print("started get distribution")
    #print n most common words for fake and for true separately
    #print_text_distribution(lemmatized_data,"content","true",15)
    #print_text_distribution(lemmatized_data,"content","fake",15)

    #   print size of csv after changing type
    new_lemmatized_data_size = pd.read_csv("data/"+new_speach_parts_file_name+".csv").shape
    new_speech_parts_data_size = pd.read_csv("data/"+new_lemmatized_file_name+".csv").shape
    print("Shape of data after lemmatize: ",new_lemmatized_data_size)
    print("Shape of speach_part data: ",new_speech_parts_data_size)
    print("Overall:",time.time()-start_time)
    
if __name__ == '__main__':
    main()

