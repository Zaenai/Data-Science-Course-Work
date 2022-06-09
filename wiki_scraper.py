import statistics
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import Libraries.database_csv as csv


def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def GA_GetDate(soup):
    try: # Need to convert from "MonthName Day, Year" to "Year-Month-Day"
        date = re.findall('[1-9]+.*[1-9]',str(soup.find("span", attrs={"id":"publishDate"})))[0]
    except:
        try: 
            date = re.findall('[A-Z][a-z]+ [0-9]+, [0-9][0-9][0-9][0-9]',str(soup.find("div", attrs={"class":"mw-parser-output"})))[0]
        except:
            date = "NaN"
    return date

def GA_GetText(soup):
    try:
        text = soup.get_text() #currently displays EVERYTHING on page, needs work
    except:
        text = "NaN"
    return text
        
def GA_GetSources(soup):
    srcs = []
    try:
        src = soup.find_all("span",attrs={"class":"sourceTemplate"})
        for n in src:
            m = remove_tags(str(n))
            srcs.append(m)      
    except:
        src = "NaN"
    return srcs
        
def GA_GetTitle(soup):
    try: 
        title = soup.find("h1",attrs={"id":"firstHeading"})
        title = remove_tags(str(title))
    except:
        title = "NaN"
    return title
        
def GA_GetContent(soup):
    try:
        article_text = ""
        article = soup.find("div",attrs={"class":"mw-parser-output"}).findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        test_text = article_text.replace("\n","")
        if test_text == "":
            test_text = re.findall('^.*(?=Have an opinion on this story?)',article_text)
            if test_text == "":
                article_text = "NaN"
            else:
                article_text = test_text
                article_text = re.sub('[A-Z][a-z]*, [A-Z][a-z]* [0-9]*, [0-9]*',"",article_text)
                article_text = re.sub('File:.*\.[a-z][a-z][a-z][a-z]?(?=)',"",article_text)
        else:
            article_text = test_text
            article_text = re.sub('[A-Z][a-z]*, [A-Z][a-z]* [0-9]*, [0-9]*',"",article_text)
            article_text = re.sub('File:.*\.[a-z][a-z][a-z][a-z]?(?=)',"",article_text)
            
    except:
        article_text = "NaN"
    return article_text
        
def GA_GetCategories(soup):
    try:
        categories = []
        cat = soup.find("div",attrs={"class":"mw-normal-catlinks"})
        cat = cat.findAll("ul")[0]
        for c in cat:
            cat = remove_tags(str(c))
            categories.append(cat)
    except:
        categories = "NaN"
    return categories

def GrabArticle(url):
    
    # init soup stuff
    response = requests.get(url)
    contents = response.text
    soup = BeautifulSoup(contents, 'html.parser')
    
    # Will try to find date, date, sources, title, text and categories, if none found/error, will return NaN
    date = GA_GetDate(soup)        
    text = GA_GetText(soup)
    srcs = GA_GetSources(soup)      
    title = GA_GetTitle(soup)
    article_text = GA_GetContent(soup) # Also removes date formatting from top of page
    categories = GA_GetCategories(soup)

    words = article_text.split()
    avg_word = sum(len(word) for word in words) / len(words)
    avg_word = round(avg_word, 2)

    return date, srcs, title, article_text, categories, avg_word

def main():

    # Initialize Group SubString
    group_nr = 14
    group_substring_raw = "ABCDEFGHIJKLMNOPRSTUVWZABCDEFGHIJKLMNOPRSTUVWZ"[group_nr%23:group_nr%23+10]
    group_substring = ""

    for letter in np.sort(list(group_substring_raw)):
        group_substring += letter
        
    print(group_substring)
    #group_substring = "Z"

    # Get main page and add subpage (according to group_substring) urls to list
    response = requests.get('https://en.wikinews.org/wiki/Category:Politics_and_conflicts')
    contents = response.text

    soup = BeautifulSoup(contents, 'html.parser')

    subpages = []
    for a in soup.find_all('a', href=True):
        for letter in group_substring:
            if "conflicts&from="+letter in a["href"]:
                if not a["href"] in subpages:
                    subpages.append(a["href"])  

    expanded_subpages = []
    for subpage in subpages:
        is_digging = True
        new_subpages = []

        while is_digging:
            curLetter = str(re.search("from=.",subpage))[-3]
            next_page = None

            response = requests.get(subpage)
            contents = response.text
            soup = BeautifulSoup(contents, 'html.parser')
            page_cands = soup.find_all('a', href=True)

            for n in page_cands:
                if "next page" in str(n):
                    next_page = n
                    if str(next_page["href"])[60] == curLetter:
                        new_subpages.append("https://en.wikinews.org/"+next_page["href"])
                    else:
                        is_digging = False
                    subpage = "https://en.wikinews.org/"+next_page["href"]
                    break
            if not next_page:
                break

        for sp in new_subpages:
            expanded_subpages.append(sp)
        
    for esp in expanded_subpages:
        subpages.append(esp)

    Articles = []
    for url in subpages:
        response = requests.get(url)
        contents = response.text

        soup = BeautifulSoup(contents, 'html.parser')

        curLetter = str(re.search("from=.",url))[-3]
        allGroups = soup.find_all("div",attrs={"class":"mw-category-group"})
        for n in allGroups:
            if "<h3>"+curLetter+"</h3>" in str(n) and "<ul><li><a" in str(n):
                pages = n
                break
        ul = re.findall('\/wiki.*(?=title)',str(pages))
        for i in range(len(ul)):
            ul[i] = "https://en.wikinews.org" + ul[i][:-2]

        Articles.append(ul)

    urls,dates,sources,titles,article_text,scraped_at,numberOfWords,categories,avg_words = [],[],[],[],[],[],[],[],[]

    articlesq = []
    statistics = []
    statistics_id  = 0
    article_id = 0
    
    for articles in Articles:
        for url in articles:
            now = datetime.now()
            
            d,s,t,at,c,aw = GrabArticle(url)
            
#            urls.append(url)
#            
#            dates.append(d)
#            sources.append(s)
#            titles.append(t)
#            article_text.append(at)
#            categories.append(c)
#            
#            avg_words.append(aw)
#        
#            numberOfWords.append(len(at.split()))
#            scraped_at.append(now.strftime("%d/%m/%Y %H:%M:%S"))
            articlesq.append([article_id, t, c, at, d, url, s, now.strftime("%d/%m/%Y %H:%M:%S")])
            statistics.append([statistics_id,article_id,aw, len(at.split())])
            statistics_id += 1
            article_id += 1
    
    articlesq_df = pd.DataFrame(articlesq, columns=["id","titles","category","content", "date", "url", "source", "scraped_at"])
    statistics_df = pd.DataFrame(statistics, columns=["id", "article_id", "avg_words", "numberofwords"])
#    Task4df = pd.DataFrame(data = {"Title" : titles,  "(Raw) No. Words" : numberOfWords, "(Raw) Avg. Word Length" : avg_words, "Date written" : dates, "Content": article_text, "Categories" : categories , "URL" : urls, "Sources" : sources, "Scraped at" : scraped_at})
    
    articlesq_df.to_csv('data/wiki_articles', index=False)
    statistics_df.to_csv('data/wiki_statistics', index=False)    
#    Task4df.to_csv('data/wiki_scraped.csv', index=False)

if __name__ == '__main__':
    main()