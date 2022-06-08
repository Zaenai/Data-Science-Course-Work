import pandas as pd
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.simple_statistics as statistics

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

def process_function(data,my_index):
    
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

    data.to_csv(f"data/contentReadyToClean{my_index + 1}.csv", encoding='utf-8', index=False)
    print("Difference:", data.shape[0]-old_rows)

def main():
    #6.8 min for milion

    #   specify number of processes
    numberOfProc = 8
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of new csv file with cleaned data
    new_file_name = "ContentReadyToClean" 

    # Read data, drop usless 
    # ONLY content, title and type left!
    data = pd.read_csv("data/NewTypesRaw.csv" ,nrows = rows)
    data = data.filter(['id','content','type'])
    data = data.astype({"id":'int32', "content":'object','type' : 'int8'})

    # use multiprocessing 
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/contentReadyToCleanX","data/"+new_file_name)
if __name__ == '__main__':
    main()