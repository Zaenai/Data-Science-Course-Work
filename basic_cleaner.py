
import imp
import pandas as pd
import time
from Libraries.simple_statistics import get_multi_features
import manage_data as md
import multiprocess as proces
import manage_csv as mcsv
import cleaning
import simple_statistics

# gets a chunk of data, cleans it and saves as 
def process_function(data,my_index):
    df = pd.DataFrame()#Dataframe with content features
    df["avg_sentence_len"] = simple_statistics.get_num_sentences(data["content"])#Initially set the column to the number of sentences
    cleaning.clean_column(data,"content")
    df["avg_word_len"], df["lexical_diversity"], df["word_count"], df["vowel_count"], df["min_three_vowels"] = get_multi_features(data["content"]).T
    #Normalizing features
    df["avg_sentence_len"] = df["avg_sentence_len"]/df["word_count"]
    df["vowel_count"] = df["vowel_count"]/df["word_count"]
    df["min_three_vowels"] = df["min_three_vowels"]/df["word_count"]
    df.to_csv(f"data/content_features{my_index + 1}.csv", encoding='utf-8', index=False)
    cleaning.clean_column(data,"title")
    #data=data[["content","title"]]
    data.to_csv('data/cleaned_part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)


def main():
    numberOfProc = 8

    #   Read data, drop usless ONLY content, title and type left!
    # data = pd.read_csv(r"data/1mio-raw.csv" ,nrows = 1000)
    # md.drop_useless_data(data)
    # data = data.filter(['content', 'title','type'])

    #   use multiprocessing to make basic clean
    # process_list = proces.make_processes(data, numberOfProc, process_function)
    # print(proces.run_proc(process_list))

    #   concatanate files
    #mcsv.conc_csv_Files(numberOfProc,"data/cleaned_partX","data/BasicCleaned")


if __name__ == '__main__':
    main()