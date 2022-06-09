from multiprocessing import Process
import math
import time
import multiprocessing
import Libraries.manage_csv as mcsv 
import pandas as pd
import Libraries.FeaturesFunctions as feat

#creates and returns numbOfProc processes
#each runs ProcFun(data/numbOfProc)
def make_processes(data,numbOfProc,ProcFun,):
    processes = list()
    step = math.floor(data.shape[0]/numbOfProc)
    print("size before split: ",data.shape[0])
    for index in range(numbOfProc):
        data_part = None
        #get chunk of data
        if (index == 0): data_part = data[0:step]
        elif (index == numbOfProc): data_part = data[(index*step):data.shape[0]]
        else: data_part = data[(index*step):(index+1)*step]    
        #create a procces and append to processes
        p = Process(target=ProcFun, args=(data_part,index ))
        processes.append(p)
    return processes

# creates numbOfProc and returns  a tuple 
# (processes,return_dictionary)
def make_processes_with_return(data, numbOfProc, ProcFun):
    manager = multiprocessing.Manager()
    ret_dict = manager.dict()
    processes = list()
    step = math.floor(data.shape[0]/numbOfProc)
    print("size before split: ",data.shape[0])
    for index in range(numbOfProc):
        data_part = None
        #get chunk of data
        if (index == 0): data_part = data[0:step]
        elif (index == numbOfProc): data_part = data[(index*step):data.shape[0]]
        else: data_part = data[(index*step):(index+1)*step]    
        #create a procces and append to processes
        p = Process(target=ProcFun, args=(data_part,index,ret_dict))
        processes.append(p)
    return (processes,ret_dict)

#runs processes and waits until all finish
# returns run-time for all proc
def run_proc(processes):
    start_time = time.time()
    #start processes
    for index, procces in enumerate(processes):
        procces.start()
        print("Process ",index, " started")
    #wait until finished
    for index, procces in enumerate(processes):
        procces.join()
        print("Process ",index, " finished")
    stop_time = time.time()
    return stop_time - start_time


def MakeNRunMultiProcess(numb_of_processes, process_fun,file_from,file_to,file_to2 = "",rows=1000000):
    def main():
        #   specify name of new csv file with cleaned data
        data = pd.read_csv(file_from ,nrows = rows)

        # WHATCH FOR TYPE CASTING AND FILTERING !
        # if preclean, typechanger, dropper, basiccleaner, rowdropper ,simple 
        if(process_fun != feat.preCleanFeatures and process_fun != feat.typeChange):
            data = data.filter(['id','content','type'])
            data = data.astype({"id":'int32', "content":'object','type' : 'int8'})
        else:
            data = data.filter(['id','content','type'])
            data = data.astype({"id":'int32', "content":'object','type' : 'object'})

        # use multiprocessing 
        process_list = make_processes(data, numb_of_processes, process_fun)
        print(run_proc(process_list))

        # concatanate files
        mcsv.conc_csvs_by_rows(numb_of_processes,"data/partX",file_to)
        try:
            mcsv.conc_csvs_by_rows(numb_of_processes,"data/part2X",file_to2)
        except:
            pass

    if __name__ == '__main__':
        main()
