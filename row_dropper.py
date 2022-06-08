import pandas as pd
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.simple_statistics as statistics


def process_function(data,my_index):
    old_rows = data.shape[0]
    toDrop = pd.read_csv("data/tooShort.csv")["shortIndex"]
    toDrop = toDrop.astype(int)
    for i in toDrop:
        try:
            data.drop(index=i, inplace = True)
        except Exception as e:
            pass
    #data.drop(data.index[toDrop.tolist()], inplace = True)
    # for index in toDrop:
    #     data.drop(axis = "index", index= int(index))
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
    data = pd.read_csv(r"data/1mio-raw.csv" ,nrows = rows)
    data = data.filter(['content','type'])

    # use multiprocessing 
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/contentReadyToCleanX","data/"+new_file_name)
if __name__ == '__main__':
    main()