from nltk.probability import FreqDist
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def get_fake_text_distribution(data, col):
    fake_text = ""
    fake = data.loc[data['type'] == 0]
    for text in fake[col]:
        fake_text += " " + text
    return FreqDist(fake_text)

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
        return wordnet.NOUN 

def lemmatise_text(text): 
    buff = word_tokenize(text)
    buff = nltk.pos_tag(buff)
    lemmatizer = WordNetLemmatizer()
    lemmatised = []
    for index, word in enumerate(buff):
        buff[index] = (word[0], switchTag(word[1]))
        lemmatised.append(lemmatizer.lemmatize(buff[index][0],pos=buff[index][1]))
    return lemmatised

eng_stopwords = stopwords.words('english')
#Find the frequency distribution for every type, eg. frequency distribution when looking at all fake news articles concatenated 
text_distribution = get_complete_text_distribution("content")
 
def getFakeWordDist(data):
    # lematise 
    text_distribution[type] = lemmatise_text(text_distribution[type])
    # Delete stop-words
    text_distribution[type] = [word for word in text_distribution[type] if word not in eng_stopwords]
    # create freqDist object 
    text_distribution[type] = FreqDist(text_distribution[type])