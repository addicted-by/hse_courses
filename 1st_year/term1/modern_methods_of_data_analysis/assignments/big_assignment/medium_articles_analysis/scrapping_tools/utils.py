from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import lxml
from bs4 import BeautifulSoup
import asyncio
from .scrapper import *
import csv 
import pandas as pd
from tqdm import tqdm
import csv
import numpy as np
import os
import threading

columns = ['title', 'link', 'publication', 'author', 'followers', 
            'reading_time', 'n_words', 'pure_text', 'date', 
            'responses', 'n_code_chunks', 'bold_text_count', 
            'italic_text_count', 'mean_image_width', 'mean_image_height', 
            'n_images', 'n_lists', 'n_vids', 'n_links', 'claps']



def scrape_page(link, options, csv_writer=None, compare:bool=False, idle_row:pd.Series=None):
    page_url = link

    driver = webdriver.Edge(options=options)
    try:
        driver.get(page_url)
    except:
        print('Time out')
        res = {
            "title": None,
            "publication": None,
            "link": link,
            "author": None,
            "followers": None,
            "reading_time": None,
            "n_words": None,
            "pure_text": None,
            #"blockquotes": self.get_blockquotes(soup),
            "date": None,
            "responses": None,
            "n_code_chunks": None,
            "bold_text_count": None,
            "italic_text_count": None,
            "mean_image_width": None,
            "mean_image_height": None,
            "n_images": None,
            "n_lists": None,
            #"n_gists": self.count_gists(soup),
            "n_vids": None,
            "n_links": None,
            "claps": None
        }, 0
        if csv_writer:
            if compare:
                for col in idle_row.keys():
                    if res[col] == None:
                        res[col] = idle_row[col]
                        print(col, "filled by initial data")
            csv_writer.writerow(res.values())
        return res, 0
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    article_scrapper = ArticleScraper()
    res = article_scrapper.scrape(soup=soup, link=link)
    if csv_writer:
        if compare:
            for col in idle_row.keys():
                if res[col] == None:
                    res[col] = idle_row[col]
                    print(col, "filled by initial data")
        csv_writer.writerow(res.values())
    return res, soup


def scrap_articles_csv(df: pd.DataFrame,  
                columns:list=columns, options=None, rows: int=50,
                path:str="./scrapped_data/scrapped_data.csv"):
    
    if os.path.exists(path):
        df_scrapped = pd.read_csv(path)
    else:
        df_scrapped = pd.DataFrame(columns=columns).to_csv()
    count = 0
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        res, _ = scrape_page(row['link'], options)
        print(count, df.shape[0])
        for col in df.columns:
            if res[col] == None:
                res[col] = row[col]
        df_scrapped.loc[df_scrapped.shape[0], :] = res   
        if (count % rows == 0 or count == df.shape[0] - 1):
            print("Saving to" + path)
            df_scrapped.to_csv(path, index=False)
        count += 1
    return df_scrapped

def chunker(seq, size):
    for pos in range(0, len(seq), size):
        yield seq.iloc[pos:pos + size] 

def chunker_list(seq, size):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size] 


def scrap_articles_async(df:pd.DataFrame, 
                        options=None, columns:list=columns, pools:int=5,
                        path:str="./scrapped_data/scrapped_async_data_part3.csv"):
    links = df["link"].values
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path)
    with open(path, "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        for chunk in tqdm(chunker(df, pools), total=df.shape[0] // pools):
            tasks = []
            for _, row in chunk.iterrows():
                tasks.append(threading.Thread(target=scrape_page, args=(row["link"], options, csv_writer, True, row, )))
                
            for task in tasks:
                task.start()
            for task in tasks:
                task.join()

def scrap_articles_async_list(links:list, options=None, columns:list=columns, pools:int=5,
                              path:str="./scrapped_data/scrapped_async_data_part7.csv"):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path)
    with open(path, "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        for chunk in tqdm(chunker_list(links, pools), total=len(links) // pools):
            tasks = []
            for link in chunk:
                tasks.append(threading.Thread(target=scrape_page, args=(link, options, csv_writer, )))
                
            for task in tasks:
                task.start()
            for task in tasks:
                task.join()