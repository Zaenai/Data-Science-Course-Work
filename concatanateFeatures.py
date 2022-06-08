
import pandas as pd

def FindIndexesToDrop(features_data):
    indx_to_Drop = []
    for index,entry in zip(features_data["word_count"].index,features_data["word_count"]):
        if(entry == 1):
            indx_to_Drop.append(index)
    return indx_to_Drop

features_post_lemma = pd.read_csv("features/FeaturesLemmatized.csv")
print(features_post_lemma.columns)
toDrop = FindIndexesToDrop(features_post_lemma)

allFeatures = features_post_lemma.drop(axis=0,index=toDrop,inplace=True)

files_lst=["features/FeaturesPreCleanAfterDrop.csv","features/FeaturesPostClean.csv","data/Speech_Parts.csv"]

for i in range (3):
    new_csv = pd.read_csv(files_lst[i])
    print(new_csv.columns)
    new_csv= new_csv.drop(axis=0,index=toDrop,inplace=True)
    allFeatures = pd.concat([allFeatures,new_csv],ignore_index=True,axis=1)

allFeatures.to_csv("allFeatures",encoding='utf-8', index=False)