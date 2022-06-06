from hashlib import new
import pandas as pd
import re
import math
import os

#concatanate numberOfFiles csv named nameFormat by rows
# files and saves as targetName.csv
# nameformat example: "data_partX"
def conc_csvs_by_rows(numberOfFiles,nameFormat, targetName, deleteParts=True):
    data = None
    for i in range(1,numberOfFiles+1):
        nameToRead = re.sub(r'X+', str(i), nameFormat)+".csv"
        if (i==1):
            if(os.path.isfile(nameToRead)): 
                data = pd.read_csv(nameToRead)
                os.remove(nameToRead)
            else: 
                print("Error: file ", nameToRead, "does not exist ! ")
        else:
            if(os.path.isfile(nameToRead)): 
                data = data.append(pd.read_csv(nameToRead),ignore_index=True)
                os.remove(nameToRead)
            else:
                print("Error: file ", nameToRead, "does not exist ! ")
    data.to_csv(targetName+".csv", encoding='utf-8', index=False)


#splits csv to numberOfFiles parts
# nameformat example: "data_partX"
def split_csv(file,numberOfFiles,nameFormat):
    data = pd.read_csv(file+".csv")
    step = math.floor(data.shape[0]/numberOfFiles)
    for index in range(numberOfFiles):
        data_part = None
        #get chunk of data
        if (index == 0): data_part = data[0:step]
        elif (index == numberOfFiles): data_part = data[(index*step):data.shape[0]]
        else: data_part = data[(index*step):(index+1)*step]
        new_name = re.sub(r'X', str(index), nameFormat)+".csv" 
        data_part.to_csv(new_name, encoding='utf-8', index=False)


# concatanate numberOfFiles csv named nameFormat by columns 
# files and saves as targetName.csv
# nameformat example: "data_partX"
def conc_csvs_by_columns(numberOfFiles,nameFormat, targetName, deleteParts=True):
    data = None
    for i in range(1,numberOfFiles+1):
        nameToRead = re.sub(r'X+', str(i), nameFormat)+".csv"
        if (i==1):
            if(os.path.isfile(nameToRead)): 
                data = pd.read_csv(nameToRead)
                os.remove(nameToRead)
            else: 
                print("Error: file ", nameToRead, "does not exist ! ")
        else:
            if(os.path.isfile(nameToRead)): 
                data = pd.concat([data,pd.read_csv(nameToRead)],ignore_index=True,axis=1)
                os.remove(nameToRead)
            else:
                print("Error: file ", nameToRead, "does not exist ! ")
        
    data.to_csv(targetName+".csv", encoding='utf-8', index=False)
