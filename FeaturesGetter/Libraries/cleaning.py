
import re 
from cleantext.sklearn import CleanTransformer

initial_cleaner = CleanTransformer(fix_unicode=True,               # fix various unicode errors
                                    to_ascii=True,                  # transliterate to closest ASCII representation
                                    lower=True,                     # lowercase text
                                    no_line_breaks=True,           # fully strip line breaks as opposed to only normalizing them
                                    no_urls=True,                  # replace all URLs with a special token
                                    no_emails=True,                # replace all email addresses with a special token
                                    no_phone_numbers=True,         # replace all phone numbers with a special token
                                    no_numbers=True,               # replace all numbers with a special token
                                    no_digits=True,                # replace all digits with a special token
                                    no_currency_symbols=True,      # replace all currency symbols with a special token
                                    no_punct=True,                      # set to 'de' for German special handling
                                )

multiple_chars = r'(.)\1{3,}'
special_symbols = r'([^<>a-z ])'#Matches special symbols such as © or ™
single_letter = r' [a-z] ' #matches single letters
temp = r'<0>|<url>|<cur>|<email>|<phone>'
symbols = r'[^a-z]+' 
url = r'@+'
number = r'[0-9]+'
bracket = r'<+'
email  = r'@+'
punct_quote = r'\.+|\"+|\(+|\)+|\045+\054+|\.+|\'+'
mix = number+'|'+url+'|'+bracket+'|'+symbols
every = punct_quote+'|'+mix+'|'+multiple_chars


def clean_column(data, col_name):    
    for i, entry in zip(data[col_name].index, data[col_name]):
        cleaned = initial_cleaner.transform([entry])[0]
        if(i%500):("500 done")
        cleaned = cleaned.split()
        #print(cleaned)
        #for each word
        for j in range (len(cleaned)):
            word = cleaned[j]
            # delete: " ' () .
            while(re.match(punct_quote,word)!=None):
                word = re.sub(punct_quote,"",word)
            #     print(cleaned[j]," changed to", word)
            #delete if <>, number, symbols etc.
            if (re.match(mix,word)!=None or len(word) < 2):
                    #print("deleted:", word)
                    cleaned[j] = ""
        cleaned  = " ".join(cleaned)
        data[col_name][i] = cleaned


