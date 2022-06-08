
import pandas as pd
import numpy as np
from regex import D
# def FindIndexesToDrop(features_data):
#     indx_to_Drop = []
#     for index,entry in zip(features_data["word_count"].index,features_data["word_count"]):
#         if(entry == 1):
#             indx_to_Drop.append(index)
#     return indx_to_Drop

# features_post_lemma = pd.read_csv("features/FeaturesLemmatized.csv")
# print(features_post_lemma.columns)
# toDrop = FindIndexesToDrop(features_post_lemma)

# allFeatures = features_post_lemma.drop(axis=0,index=toDrop)

# files_lst=["features/FeaturesPreCleanAfterDrop.csv","features/FeaturesPostClean.csv","data/Speech_Parts.csv"]
# #df.rename(columns={"A": "a", "B": "c"})
# allFeatures_cols = allFeatures.columns
# for i in range (3):
#     new_csv = pd.read_csv(files_lst[i])
#     print("next csv cols: ",new_csv.columns)
#     new_csv= new_csv.drop(axis=0,index=toDrop)
#     new_csv_cols = new_csv.columns
#     for col in new_csv_cols:
#         if col in allFeatures_cols :
#              allFeatures[col+"Post_clean"]=new_csv[col]
#         else: allFeatures[col]=new_csv[col]

#     #allFeatures = pd.concat([allFeatures,new_csv],ignore_index=True,axis=1)


#allFeatures.to_csv("features/allFeatures.csv",encoding='utf-8', index=False)

# print(allFeatures.shape)
# allcols= allFeatures.columns
# print(allFeatures.columns)

# allFeatures = allFeatures.replace([np.inf, -np.inf], np.nan).dropna(subset=["avg_sentence_len", "avg_sentence_len_Post_clean"], how="all")
# allFeatures.to_csv("features/allFeaturesRound.csv",encoding='utf-8', index=False)



# allcols= allFeatures.columns
# for colname in allcols:
#     allFeatures[colname] =  allFeatures[colname].round(3)
#     #col = allFeatures[colname]
#     #new_col = np.zeros(col.shape)
#     # for index,entry in zip(col.index,col):
#     #     allFeatures.at[colname,index]=round(entry,3)
# allFeatures.to_csv("features/allFeaturesRound.csv",index=False )


def DropTurboFeature(data, cut_percent_total):
    cut_per = cut_percent_total/2
    for col_name in data:
        min = data[col_name].min()
        max = data[col_name].max()
        col = data[col_name]
        drop_idxs = data.loc[col > max*(1-cut_per)].index 
        data = data.drop(drop_idxs)
        drop_idxs = data.loc[col < min*(1-cut_per)].index
        data = data.drop(drop_idxs)
    return data

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.decomposition import PCA

train_features = pd.read_csv("features/allFeaturesRound.csv")
# allFeatures = pd.DataFrame(StandardScaler().fit_transform(allFeatures.to_numpy()))
# allFeatures =  DropTurboFeature(allFeatures, 0.01)
# allFeatures.to_csv("features/allFeatureStandard.csv",encoding='utf-8', index=False)


# all_features = pd.read_csv("features/allFeatures.csv")
# print(all_features.columns)
# train_features = pd.read_csv("features/allFeaturesStandard.csv")
# train_chosen = train_features[["lexical_diversity_Post_clean","vowel_count_lemma","avg_word_len_lemma","word_count_lemma"]]
# train_chosen.to_csv("features/FeaturesChosen.csv")



n_pcs= len(train_features.columns)
model = PCA(n_components=n_pcs)
model.fit(train_features)

X_pc = model.transform(train_features)

most_important = [np.abs(model.components_[i]).argmax() for i in range(n_pcs)]
print(most_important)
initial_feature_names = list(all_features.columns)
most_important_names = [initial_feature_names[most_important[i]] for i in range(n_pcs)]
dic = {'PC{}'.format(i+1): most_important_names[i] for i in range(n_pcs)}
df = pd.DataFrame(sorted(dic.items()))
df["evr"] = model.explained_variance_ratio_
print(df)
for val in df["evr"]:
    print(round(val, 4))



#"print (allFeatures[:][:10])
#'{0:f}'.format(x/y)




