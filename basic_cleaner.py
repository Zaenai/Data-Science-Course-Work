
import imp
import pandas as pd
import time
import manage_data as md
import multiprocess as proces
import manage_csv as mcsv
import cleaning

# gets a chunk of data, cleans it and saves as 
def process_function(data,my_index):
    cleaning.clean_column(data,"content")
    cleaning.clean_column(data,"title")
    #data=data[["content","title"]]
    data.to_csv('data/cleaned_part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)


def main():
    numberOfProc = 8

    data = pd.read_csv(r"data/1mio-raw.csv", nrows = 100000)
    md.drop_useless_data(data)

    process_list = proces.make_processes(data,numberOfProc,process_function)
    print(proces.run_proc(process_list))


    #checkFilesLengths(max_processes)
    mcsv.conc_csv_Files(numberOfProc,"data/cleaned_partX","data/cleanedComplete")


    complete_data = pd.read_csv('data/cleanedComplete.csv')

    print(data["content"][0])
    print(complete_data["content"][0])

if __name__ == '__main__':
    main()