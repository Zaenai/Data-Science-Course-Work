import pandas as pd
from Libraries.simple_statistics import get_multi_features
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.simple_statistics as statistics



# gets a chunk of data, cleans it and saves as 
def process_function(data,my_index):
    #data.dropna(subset = ["content"], inplace = True)

    numb_of_sentences = pd.read_csv(r"features/FeaturesPreClean.csv" ,skiprows=data.first_valid_index(), skipfooter=data.last_valid_index())
    numb_of_sentences = numb_of_sentences.iloc[:, 1]
    #numb_of_sentences = numb_of_sentences["num_sentences"]
    
    #Dataframe with content features
    df = pd.DataFrame()
    df["avg_word_len"], df["lexical_diversity"], df["word_count"], df["vowel_count"], df["min_three_vowels"] = get_multi_features(data["content"]).T
    print(df["word_count"])
    
    #Normalizing features
    df["avg_sentence_len"] = df["word_count"]/numb_of_sentences
    df["vowel_count"] = df["vowel_count"]/df["word_count"]
    df["min_three_vowels"] = df["min_three_vowels"]/df["word_count"]
    df.to_csv('features/content_features'+str(my_index+1)+'.csv', encoding='utf-8', index=False)


def main():
    #   specify number of processes
    numberOfProc = 8
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of new csv file with cleaned data
    new_file_name = "FeaturesLemmatized"#"FeaturesPostClean"

    #data = pd.read_csv(r"data/NewTypesCleaned.csv" ,nrows = rows)
    data = pd.read_csv(r"data/Lemmatized.csv" ,nrows = rows)
    
    # use multiprocessing to make basic clean
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"features/content_featuresX","features/"+new_file_name)

if __name__ == '__main__':
    main()

    