 
from nltk.probability import FreqDist
import pandas as pd 
import Libraries.manage_csv as mcsv
import Libraries.multiprocess as proces

def process_function(data,my_index):
    changeTypes(data)
    data.to_csv('data/newTypes_part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)

def isNonFake(t):
    return 1 if t in ["political", "reliable"] else 0

def changeTypes(data):
    data["type"] = data["type"].map(isNonFake)
            

def main():

    #   specify number of processes
    numberOfProc = 8
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of new csv file with cleaned data
    new_file_name = "NewTypesRaw"

    #   read data
    data = pd.read_csv(r"data/raw.csv",nrows = rows)
    data = data[["id","content","type"]]
    
    #   use multiprocessing to make basic clean
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    #   concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/newTypes_partX","data/"+new_file_name)

    #   print size of csv after changing type
    #new_data = pd.read_csv("data/"+new_file_name+".csv")
    #print("Shape of data after changing type: ",new_data.shape)

if __name__ == '__main__':
    main()