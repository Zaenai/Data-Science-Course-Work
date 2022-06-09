import math

#splits data to numberOfParts parts
#and returns a list of frames 
def split_data(data,numberOfParts):
    data_list = list()
    step = math.floor(data.shape[0]/numberOfParts)
    for index in range(numberOfParts):
        data_part = None
        #get chunk of data
        if (index == 0): data_part = data[0:step]
        elif (index == numberOfParts): data_part = data[(index*step):data.shape[0]]
        else: data_part = data[(index*step):(index+1)*step]
    data_list.append(data_part)

# drops columns: "Unnamed: 0","id","scraped_at","inserted_at","updated_at"
# drop rows with type = nan and type = unknown

def drop_useless_data(data):
    #Dropping unneeded columns
    # cols_to_delete = ["Unnamed: 0","id","scraped_at","inserted_at","updated_at"]
    # for column in data.columns:
    #     if data[column].isnull().values.all():
    #         cols_to_delete.append(column)
    # data.drop(cols_to_delete, 1, inplace=True)
    
    #Dropping entries with nan type
    data.dropna(subset = ["type", "content"], inplace = True)
    #Dropping entries with unknown type
    data.drop(data.loc[data["type"] == "unknown"].index, inplace=True)
    print("rows after initial  drop:", data.shape[0])



