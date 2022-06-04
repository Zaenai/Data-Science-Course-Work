import re
import numpy as np
    
    #count number of sentences. (use before base clean)
    def get_num_of_sentences(content):
        result = np.empty()
        multi_period = r'\.{2,}'
        #Replacing multiple periods with a single, ie. "..." -> "." 
        for t in content:
            text = re.sub(multi_period, ".", t)
            count = 0
            for s in text.split("."):
                if s != "":
                    count += 1
            result[]

    #calculates lexical div and avrg word length
    def lex_div_count(content):
        result = np.empty(shape=(len(content), 2))
        word_count=0
        words_lengths = 0
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
                    if word not in seen_words:
                        num_unique_words += num_unique_words
                #average word length
            result[i][0] = words_lengths/word_count
            #lex div
            result[i][1] = num_unique_words/word_count
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