from multiprocessing import Process
import math
import time
import multiprocessing

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