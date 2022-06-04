import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import wordnet
from nltk.corpus import stopwords
#nltk.download('all')
str = "donald trump has the unnerving ability to ability to create his own reality and convince millions of americans that what he says it is true the problem with the president lying is that he then believes his own lies a new poll shows how that can get the country into deep trouble the new abc news washington post poll came out after the president s physician gave him a physical and mental exam the doctor gave trump a clean bill of health added an inch to his height and claimed he was fit to serve for seven more years this poll was able to capture americans opinions after a new book came out indicating that people around trump questioned his emotional stability and ability to hold office in addition the new poll gave the respondents the time to hear trump tell the public that he was a very stable genius before they were interviewed he said actually throughout my life my" 
str2 = "two greatest assets have been mental stability and being like really smart the abc washington post poll discovered that <number> percent of the people it interviewed believed that the president was a genius that left a full <number> percent who saw through that lie then there was the question of trump s mental stability the poll found that there was a nearly even divide throughout the nation when asked if the president was stable <number> percent of those interviewed said he was not but <number> percent believed he is stable the abc news washington post poll was taken from <date> through <number> <number> the random sample consisted of <number> adults interviewed by landline and cell phone in both english and spanish the margin of error was  <number> <number> percentage points featured image via getty images drew angerer"

lemmatizer = WordNetLemmatizer()


def WordFreq(col_name, article_number, input):
    q = input[col_name][article_number]
    unique_words = set(q)
    unique_word_count = len(unique_words)
    qqq = len(q)/unique_word_count
    return qqq

def WordFreqSet(set_value , set_data):
    WordFreqArray = []
    for col in set_data.index:
        WordFreqArray.append(WordFreq(set_value, col, set_data))
    return WordFreqArray


# switch tags, compatibility with lemmatise() 
def switchTag(tag):
    if tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('V'):
        return wordnet.VERB
    elif (tag.startswith('J') or
            tag.startswith('A')):
        return wordnet.ADJ
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        print(tag)
        return wordnet.NOUN #''

# lemmatise with respect to tag
def lemmatisation(str,lemmatizer,type):
    str_token = word_tokenize(str)
    retVal = []
    for word in str_token:
        retVal.append(lemmatizer.lemmatize(word,pos=type))
    return retVal


# # Use it to count dates/numbers 
# tx = "<date> and not date <date>"
# tx = tx.replace('<date>','')
# difference between old and new tx is number of dates

tx = ""
tx = tx.replace('<date>','')
tx = tx.replace('<number>','')
tx = word_tokenize(tx)

eng_stopwords = stopwords.words('english')
tx = [word for word in tx if word not in eng_stopwords]


# CD are numbers ; IN can be 'around' or 'like', 'via' etc.
# use it at some point to calculate the real number of <numbers> 
tx = nltk.pos_tag(tx)
        
for index,word in enumerate(tx):
     tx[index] = (word[0],switchTag(word[1]))

for index,word in enumerate(tx):
    tx[index] = lemmatizer.lemmatize(word[0],pos=word[1])


# print(tx)










# print(len(str_lemma))
# print(len(str_lemma2))
# print(len(set(str_lemma)))
# print(len(set(str_lemma2)))

# print(len(set(str_big_lemma)))

# freq = FreqDist(str_big_lemma)
# print(freq.most_common(15))


# from nltk.corpus import wordnet as wn
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk import word_tokenize, pos_tag
# from collections import defaultdict

# tag_map = defaultdict(lambda : wn.NOUN)
# tag_map['J'] = wn.ADJ
# tag_map['V'] = wn.VERB
# tag_map['R'] = wn.ADV

# text = "Another way of achieving this task"
# tokens = word_tokenize(text)
# lmtzr = WordNetLemmatizer()

# for token, tag in pos_tag(tokens):
#     lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
#     print(token, "=>", lemma)