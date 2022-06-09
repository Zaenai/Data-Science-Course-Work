
from numpy import NaN
import Libraries.multiprocess  as multiproc
import Libraries.FeaturesFunctions as feat
import pandas as pd
from multiprocessing import Process
import Libraries.manage_csv as mcsv 
import pandas as pd
import Libraries.FeaturesFunctions as feat
import os

def MakeNRunMultiProcess(numb_of_processes, process_fun,file_from,file_to,file_to2 = "",rows=1000000):
    
    #   specify name of new csv file with cleaned data
    data = pd.read_csv(file_from ,nrows = rows)

    if(process_fun != feat.preCleanFeatures and process_fun != feat.typeChange):
        data = data.filter(['id','content','type'])
        data = data.astype({"id":'int32', "content":'object','type' : 'int8'})
    else:
        data = data.filter(['id','content','type'])
        data = data.astype({"id":'int32', "content":'object','type' : 'object'})

    # use multiprocessing 
    process_list = multiproc.make_processes(data, numb_of_processes, process_fun)
    print(multiproc.run_proc(process_list))

    # concatanate files
    mcsv.conc_csvs_by_rows(numb_of_processes,"data/partX",file_to)
    if(file_to2 != ""):
        try:
            mcsv.conc_csvs_by_rows(numb_of_processes,"data/part2X",file_to2)
        except:
            pass



def main(num_proc,rows_to_read,fromfile='data/1mio-raw.csv'):
    if __name__ == '__main__':
        
        raw = pd.read_csv(fromfile,nrows = rows_to_read)
        index= raw.index
        raw["id"] = index
        raw.to_csv("data/raw.csv",index=False)

        #preClean features
        print("PRE CLEAN STARTED------")
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.preCleanFeatures,
                                        file_from= "data/raw.csv",
                                        file_to= "features/FeaturesPreClean",
                                        file_to2= "data/tooShort", rows= rows_to_read )  
        
        print("TYPE CHANGER STARTED------")
        #type Changer
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.typeChange,
                                        file_from= "data/raw.csv",
                                        file_to= "data/NewTypesRaw",
                                        rows= rows_to_read )  
        

        print("DROP SHORT CONTENT STARTED------")
        #row dropper
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.dropToShortRows,
                                        file_from= "data/NewTypesRaw.csv",
                                        file_to= "data/ContentReadyToClean",
                                        rows= rows_to_read )  
        
        
        print("basic clean started")
        #basic clean
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.basicClean,
                                        file_from= "data/ContentReadyToClean.csv",
                                        file_to= "data/BasicCleaned",
                                        rows= rows_to_read )  
        
        
        print("simple feature on cleaned started")
        #simple feature
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.simple_feature,
                                        file_from= "data/BasicCleaned.csv",
                                        file_to= "features/FeaturesPostClean",
                                        rows= rows_to_read )  
        
        print("speech parts started")
        #speech parts
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.speech_parts,
                                        file_from= "data/BasicCleaned.csv",
                                        file_to= "features/Speech_Parts",
                                        file_to2= "data/Lemmatized",
                                        rows= rows_to_read )  
        
        print("simple feature on lemmatized started")
        #simple feature
        MakeNRunMultiProcess(num_proc,
                                        process_fun = feat.simple_feature,
                                        file_from= "data/Lemmatized.csv",
                                        file_to= "features/FeaturesPostLemmatized",
                                        rows= rows_to_read )  
        

        feat.ConcatanateNTransformFeatures()



if __name__ == '__main__':
    main( num_proc=8 , fromfile="data/1mio-raw.csv",rows_to_read=10000)