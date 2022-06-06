 
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

    numberOfProc = 8

    # #   read data
    # data = pd.read_csv(r"data/BasicCleanedMILION.csv",nrows = 100)
    
    
    # #  use multiprocessing to make basic clean
    # process_list = proces.make_processes(data, numberOfProc, process_function)
    # print(proces.run_proc(process_list))

    # #   concatanate files
    #mcsv.conc_csvs_by_rows(numberOfProc,"data/newTypes_partX","data/NewTypesCleanedMilion")

if __name__ == '__main__':
    main()