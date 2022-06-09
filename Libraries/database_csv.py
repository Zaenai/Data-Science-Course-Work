import numpy as np
import pandas as pd
from pathlib import Path

article_keyword_list = []
keywords_dict = {"['']":0}
article_author_list = [] #Ends up containing lists [article id, author name]
author_id = 0
author_dict = {"nan":0}
tag_list = []
tags_id = 0
tags_dict = {"nan":0}
articles = []
has_written_list = []

def string_to_list(s):
    l = s.strip('][').split(', ')
    return [w.strip("'").lower() for w in l]

def get_csvs(data):
    for i, article in data.iterrows():
        article_id = int(article["id"])

        for word in string_to_list(article["meta_keywords"]):
            if word == "['']":
                article_keyword_list.append([0, article_id, np.nan])
                continue
            if not word in keywords_dict:
                keyword_id += 1
                keywords_dict[word] = keyword_id
                
            article_keyword_list.append([keywords_dict[word], article_id, word])

        for author in string_to_list(article["authors"]):
            if str(article["authors"]) == "nan":
                article_author_list.append([0, article_id, np.nan])
                continue
            if author not in author_dict:
                author_id += 1
                author_dict[author] = author_id
        
            article_author_list.append([author_dict[author], article_id, author])
            has_written_list.append([author_dict[author], article_id])
            
        for tag in string_to_list(article["tags"]):
            if str(article["tags"]) == "nan":
                tag_list.append([0, article_id, np.nan])
                continue
            if tag not in tags_dict:
                tags_id += 1
                tags_dict[tag] = tags_id
    
            tag_list.append([tags_dict[tag], article_id, tag])
                

        clean = article["content"].replace("\n", "")
        cleaned = clean.replace('"', "")
        articles.append([article["id"],
                        article["domain"], 
                        article["type"],
                        article["url"],  
                        cleaned,
                        article["scraped_at"],
                        article["inserted_at"],
                        article["updated_at"], 
                        article["title"],  
                        article["meta_description"]])

    keywords_df = pd.DataFrame(article_keyword_list, columns=["id", "article_id", "keyword"])
    authors_df = pd.DataFrame(article_author_list, columns=["id", "article_id", "author_name"])
    tags_df = pd.DataFrame(tag_list, columns=["id", "article_id", "tag"])
    article_df = pd.DataFrame(articles, columns=["article_id", "domain", "type", "url", "content", "scraped_at", "inserted_at", "updated_at", "title", "meta_description"])
    has_written_df = pd.DataFrame(has_written_list, columns=["author_id", "article_id"])

    keyword_combinations_path = Path(r"C:\Users\Peter\Ny mappe\keywords.csv")
    authors_path = Path(r"C:\Users\Peter\Ny mappe\authors.csv")
    tags_path = Path(r"C:\Users\Peter\Ny mappe\tags.csv")
    articles_path = Path(r"C:\Users\Peter\Ny mappe\articles.csv")
    has_written_path = Path(r"C:\Users\Peter\Ny mappe\has_written.csv")

    keywords_df.to_csv('data/keywords.csv', encoding='utf-8', index=False)
    authors_df.to_csv('data/authors.csv', encoding='utf-8', index=False)
    tags_df.to_csv('data/tags.csv', encoding='utf-8', index=False)
    article_df.to_csv('data/article.csv', encoding='utf-8', index=False)
    has_written_df.to_csv('data/has_written.csv', encoding='utf-8', index=False)