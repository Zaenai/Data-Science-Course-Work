
import pandas as pd
import Libraries.manage_data as md
import Libraries.multiprocess as proces
import Libraries.manage_csv as mcsv
import Libraries.cleaning as cleaning


# gets a chunk of data, cleans it and saves as 
def process_function(data,my_index):
    #cleaning
    cleaning.clean_column(data,"content")
    data.to_csv('data/cleaned_part'+str(my_index+1)+'.csv', encoding='utf-8', index=False)


def main():
    #16.9min for milion after drop rows

    #   specify number of processes
    numberOfProc = 8
    #   specify number of rows to clean
    rows = 1000000
    #   specify name of new csv file with cleaned data
    new_file_name = "BasicCleaned"

    # Read data, drop usless 
    # ONLY content, title and type left!
    data = pd.read_csv(r"data/ContentReadyToClean.csv" ,nrows = rows)
    md.drop_useless_data(data)
    data = data.filter(['content','type'])
    
    print(type(data))
    # use multiprocessing to make basic clean
    process_list = proces.make_processes(data, numberOfProc, process_function)
    print(proces.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numberOfProc,"data/cleaned_partX","data/"+new_file_name)

if __name__ == '__main__':
    main()