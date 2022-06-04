import re
import numpy as np
    
#count number of sentences. (use before base clean)
def get_get_num_sentences(content):
    return content.map(get_num_sentences_in_text)

def get_num_sentences_in_text(text):
    sentence_count = 0
    multi_period = r'\.{2,}'
    #Replacing multiple periods with a single, ie. "..." -> "." 
    text = re.sub(multi_period, ".", text)
    for s in text.split("."):
        if s != "":
            sentence_count += 1
    return sentence_count
        
def vowel_count(word):
    vowels = "aeiouyAEIOUY"
    count = 0
    for c in word:
        if c in vowels:
            count += 1
    return count


#calculates lexical div and avrg word length
def lex_div_count(content):
    result = np.empty(shape=(len(content), 5))
    word_count=0
    words_lengths = 0
    vowel_count = 0
    min_three_vowels_count = 0
    seen_words = set()
    num_unique_words = 0
    #for each article
    for i,article in zip(content.index,content):
        words = article.split(" ")
        #for each word in article
        for word in words:
            #if not empty word
            if word != "":
                word_count += 1
                words_lengths += len(word)
                vc = vowel_count(word)
                vowel_count += vc
                if vc >= 3:
                    min_three_vowels_count += 1
                if word not in seen_words:
                    num_unique_words += num_unique_words
        #average word length
        result[i][0] = words_lengths/word_count
        #lex div
        result[i][1] = num_unique_words/word_count
        result[i][2] = word_count
        result[i][3] = vowel_count
        result[i][4] = min_three_vowels_count
    return result



# basic clean on all
# save as csv
# create two TextFeatureExtractor
# one for true , one for false
# call TextFeatureExtractor.lex_div_count_avrg(true_data)



#   before basic clean:
# avrg. sentence length
# avrg. difference in lenght before cleaning and after

#   after basic:
# avrg. occurances of the most common word divided by lenght
# avrg. length of content
# number of words shorter/longer than n
# lexical diversity (num words/num unique words)

#   sentiment analysis
#avrg. positive/negatice words

#   after stemming
# avrg. difference in lenght before stemming and after
# avrg. occurances of the most common word divided by lenght
# avrg. length of content
# lexical diversity (num words/num unique words)

#   after lemmatization
# avrg. difference in lenght before stemming and after
# avrg. occurances of the most common word divided by lenght
# avrg. length of content
# lexical diversity (num words/num unique words)


#   after lemmatization:
#number of verbs,subjects etc. 