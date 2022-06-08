import pandas as pd
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.simple_statistics as statistics
import csv
import numpy as np

# Creates csv with avrg. words per sentence length BEFORE CLEANING 
def process_function(data,my_index):
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
    file = open('data/tooShort'+ str(my_index+1)+'.csv', 'w+', newline ='',encoding='UTF8') 
    with file:     
        write = csv.writer(file)
        write.writerows(too_short_articles)
    old_size = df.shape[0]
    df.drop(axis=0, index= to_drop_now, inplace=True)
    df.filter(["id","avg_sentence_len","num_sentences"]).to_csv(f"features/featuresPreClean{my_index + 1}.csv", encoding='utf-8', index=False)
    print("diff= ",old_size-df.shape[0])
def main():
    # 14 sec 

    #   specify number of processes
    numberOfProc = 2
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of new csv file with cleaned data
    new_file_name = "FeaturesPreClean"
    new_file_name_rows = "TooShort"

    data = pd.read_csv(r"data/raw.csv" ,nrows = rows)
    data = data.filter(['id','content','type'])

    # use multiprocessing 
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"features/featuresPreCleanX","features/"+new_file_name)
    mcsv.conc_csvs_by_rows(numberOfProc,"data/tooShortX","data/"+new_file_name_rows)

if __name__ == '__main__':
    main()