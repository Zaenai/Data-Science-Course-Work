import re
import csv
import numpy as np
    
#count number of sentences. (use before base clean)
def get_num_sentences(content):
    return content.map(get_num_sentences_in_text)

def get_num_sentences_in_text(text):
    sentence_count = 0
    multi_period = r'\.{2,}'
    #Replacing multiple periods with a single, ie. "..." -> "." 
    try:
        text = re.sub(multi_period, ".", text)
    except:
        return 1
    for s in text.split("."):
        if s != "":
            sentence_count += 1
    #if sentence_count == 0: return 1
    return sentence_count

def count_words(text):
    if not isinstance(text, str):
        return 1
    word_count = 0
    words = text.split(" ")
    #for each word in article
    for word in words:
        #if not empty word
        if word != "":
            word_count += 1
    if word_count == 0: return 1
    return word_count

def preclean_word_count(content):
    return content.map(count_words)
        
def vowel_cnt(word):
    vowels = "aeiouyAEIOUY"
    count = 0
    for c in word:
        if c in vowels:
            count += 1
    return count


# vectorizer = CountVectorizer(stop_words='english')
# X = vectorizer.fit_transform([doc1,doc2,doc3])

# eng_stopwords = stopwords.words('english')


#We get:
#number of words 
#average word length
#vowel count which approximates the number of syllables (to be normalized to average number of vowels per word)
#number of words with at least 3 vowels which are intuitively more complex words (to be normalized to ratio of complex words and the total number of words)
#lexical diversity, ie. the ratio between the number of unique words and the total number of words
def get_multi_features(data,my_id,makeNan = False):
    result = np.empty(shape=(len(data["content"]), 5))
    #for each article
    #for i,article in zip(range(len(content)),content):
    i = 0
    for id,article in zip(data["id"], data["content"]):
        if isinstance(article, str):
            words = article.split(" ")
            word_count=1
            words_lengths = 0
            vowel_count = 0
            min_three_vowels_count = 0
            seen_words = set()
            num_unique_words = 0
            #for each word in article
            for word in words:
                #if not empty word
                if word != "":
                    word_count += 1
                    words_lengths += len(word)
                    vc = vowel_cnt(word)
                    vowel_count += vc
                    if vc >= 3:
                        min_three_vowels_count += 1
                    if word not in seen_words:
                        num_unique_words += 1
                        seen_words.add(word)
            #average word length
            result[i][0] = words_lengths/word_count
            #lex div
            result[i][1] = num_unique_words/word_count
            result[i][2] = word_count
            result[i][3] = vowel_count
            result[i][4] = min_three_vowels_count
        else:
            # if(makeNan):
            #     f = open('part2.csv'+str(my_id+1), 'w')
            #     writer = csv.writer(f)
            #     writer.writerow([id])
            #print(f"{id},")
            result[i] = [0,0,1,0,0]
        i+=1
    return result


#   before basic clean:
# avrg. sentence length

# avrg. difference in lenght before cleaning and after

#   after basic:
# avrg. sentence length
# avrg. length of content
# occurances of the most common word divided by lenght
# number of words shorter/longer than n
# lexical diversity (num words/num unique words)

#common_fake = [trump, bitcoin...]
#ratio = count_unique_common(article)/common_fake.Length
#ratio = count_common(article)/num_words_in_article
#(common_fake.Length - word_index)/10


#   sentiment analysis
#avrg. positive/negatice words


#   after lemmatization
# avrg. difference in lenght before lemma and after
# avrg. occurances of the most common word divided by lenght
# avrg. length of content
# lexical diversity (num words/num unique words)


#   after lemmatization:
#number of verbs,subjects etc. 