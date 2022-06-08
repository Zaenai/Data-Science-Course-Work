import pandas as pd
import csv 
import numpy as np
# cleaned = pd.read_csv("data/BasicCleaned.csv",nrows=1)

# print(cleaned)
# # features = pd.read_csv("features/allFeaturesNew.csv")
# # print(features.shape)


# df = pd.DataFrame(np.array(([1, 2, 3], [4, 5, 6],[7, 8, 9])),
#                   #index=['fst', 'snd','thd'],
#                   columns=['one', 'two', 'three'])

# #         one  two  three
# # mouse     1    2      3
# # rabbit    4    5      6

# df = df.filter(['one', 'three'])
# df = df.drop(index=1,axis=1)
# df["id"] = df.index
# print(df)
# df.to_csv("garbage.csv" , index = True)
# df = pd.read_csv("garbage.csv",index_col=False)
# print(df)

# raw = pd.read_csv("data/1mio-raw.csv")
# index= raw.index
# raw["id"] = index
# raw.to_csv("data/raw.csv",index=False)


# raw_id=pd.read_csv("data/raw.csv",nrows=1)
# print(raw_id.columns)
# print(raw_id)


# df=pd.read_csv("data/BasicCleaned.csv",nrows=112773)
# print(df.columns)
# ind = df.loc[df["id"] == 112773]
# print(ind)

# df=pd.read_csv("data/1mio-raw.csv",nrows=374161)
# #print(df.columns)
# #ind = df.loc[df["id"] == 112773]
# ind = df["content"][374160]
# print(ind)

df=pd.read_csv("data/NanContent.csv", index_col=False)
df2=pd.read_csv("a.csv",index_col=False)



df = df.astype({'nanContent':'int32'})
df2 = df2.astype({'ind':'int32'})

print(df2.columns)

df = df["nanContent"]
df2 = df2["ind"]

print(df2[0])

df = df.astype(int)
df2 = df2.astype(int)

df = df.sort_values()
df2 = df.sort_values()

print(df.shape," vs ",df2.shape)
# for i in df:
#     print(i,',')

for i,j in zip(df,df2):
    if(i!=j):
        print("wrong")