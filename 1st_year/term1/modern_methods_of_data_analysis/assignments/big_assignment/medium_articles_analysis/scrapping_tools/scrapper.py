import re
from selenium import webdriver
from PIL import Image
import requests
import datetime
from bs4 import BeautifulSoup
import time


class ArticleScraper():
    """
    Scrapes all data for an article.
    """
    def __init__(self):
        self.scraper_class = 'ArticleScraper' 

    
    def get_title(self, soup):
        try:
            title = soup.find('h1').text
            return title
        
        except:
            print("Couldn't get title from article.")

    
    def get_subtitle(self, soup):
        try:
            return soup.find('section').find('h2').text
        except:
            print("Couldn't get subtitle from article.")


    def get_publication(self, soup):
        try:
            for div in soup.find_all("div"):
                if div.text == 'Published in':
                    try:
                        return div.next_element.next_element.next_element.find('p').text
                    except:
                        continue
        except:
            print("Couldn't get publication type from article.")
            return "Medium"


    def get_author(self, soup):
        try:
            return soup.find('h2', class_=r"pw-author-name").text
        except:
            print("Couldn't get title from article.") 


    def get_reading_time(self, soup):
        try:
            return int(soup.find('div', class_=r"pw-reading-time").text.split()[0])
        except:
            print("Couldn't get reading time from article.")

    def get_claps(self, soup):
        try:
            claps = soup.find_all("div", {"class": "pw-multi-vote-count"})[0].text
            tens = {'K': 10e2, 'M': 10e5, 'B': 10e8, 'k': 10e2, 'm': 10e5, 'b': 10e8}
            if (claps[-1] != 'K' and claps[-1] != 'M' 
                        and claps[-1] != 'k' and claps[-1] != 'm'
                        and claps[-1] != 'b' and claps[-1] != 'B'):
                        return int(claps)
            f = lambda x: int(float(x[:-1])*tens[x[-1]])
            return f(claps)
        except: 
            print("Can't get claps information")


    def get_responses(self, soup): 
        try:
            responses = [x.text for x in soup.find_all("span") if x.has_attr("class") and 'pw-responses-count' in x['class']][0].split()[0]
            tens = {'K': 10e2, 'M': 10e5, 'B': 10e8, 'k': 10e2, 'm': 10e5, 'b': 10e8}
            if (responses[-1] != 'K' and responses[-1] != 'M' 
                        and responses[-1] != 'k' and responses[-1] != 'm'
                        and responses[-1] != 'b' and responses[-1] != 'B'):
                        return int(responses)
            f = lambda x: int(float(x[:-1])*tens[x[-1]])
            return f(responses)
        except:
            print("Can't get responses information")


    def get_date(self, soup):
        try:
            date_string = soup.find('p', class_=r"pw-published-date").text 
            return datetime.datetime.strptime(date_string, '%b %d, %Y').strftime('%d/%m/%Y')
        except:
            print("Couldn't get date from article.") 

    def get_followers(self, soup):
        try:
            
            fol_string = [x.text for x in soup.find_all("span") if x.has_attr("class") and 'pw-follower-count' in x['class']][0].split()[0]
            tens = {'K': 10e2, 'M': 10e5, 'B': 10e8, 'k': 10e2, 'm': 10e5, 'b': 10e8}
            if (fol_string[-1] != 'K' and fol_string[-1] != 'M' 
                        and fol_string[-1] != 'k' and fol_string[-1] != 'm'
                        and fol_string[-1] != 'b' and fol_string[-1] != 'B'):
                        return int(fol_string)
            f = lambda x: int(float(x[:-1])*tens[x[-1]])
            return f(fol_string)
        except:
            print("Can't go to the followers info")    

    
    def get_mean_size(self, soup):
        try:
            pics = soup.find('section').find_all('img')#, width=True, height=True)
            sums = (0,0)
            for pic in pics:
                url = pic.get('src')
                im = Image.open(requests.get(url, stream=True).raw)
                sums = tuple(map(sum, zip(sums, im.size)))
            mean = tuple(ti//len(pics) for ti in sums)
            if len(pics) == 0:
                return (0,0)
            return mean
        except:
            print("Can't get image's sizes")
         

    def count_figures(self, soup):
        try:
            return len(soup.find('section').find_all('img'))
        except:
            print("Can't get amount of pictures")

    def get_pure_text(self, soup):
        try:
            pure_text = ''
            for unparsed in soup.find('section').find_all('p'):
                pure_text += unparsed.text
            return pure_text
        except:
            print("Can't get pure text")
    
    
    def count_words(self, soup):
        try:
           pure_text = self.get_pure_text(soup=soup)
           return len(pure_text.split())
        except:
            print("Can't get words count from the article")

    
    def count_lists(self, soup):
        try:
            return len(soup.find('section').find_all('ol')) + len(soup.find('section').find_all('ul'))
        except:
            print("Can't get lists count")
    
    def bold_text_count(self, soup):
        try:
            return len(soup.find('section').find_all('strong'))
        except:
            print("Can't get bold text count")
    

    def get_blockquotes(self, soup):
        try:
            notes = []
            blockquotes = soup.find_all('blockquote')
            for blockquote in blockquotes:
                notes.append(blockquote.text)
            return notes
        except:
            print("Couldn't get notes from article.")


    def italic_text_count(self, soup):
        try:
            return len(soup.find('section').find_all('em'))
        except:
            print("Can't get italic text count")

    def count_vids(self, soup):
        try:
            yt_vids = []
            article_soup = soup.find('article')
            for figure in article_soup.find_all('figure'):
                yt_soup = figure.find('iframe', src=re.compile('.*youtube.*'))
                if yt_soup == None:
                    continue
                else:
                    yt_vids.append(yt_soup)
                    
            return len(yt_vids)
                    
        except:
            print("Couldn't get YouTube videos.") 
    

    def count_gists(self, soup):
        try:
            gists = []
            article_soup = soup.find('article')
            for fig in article_soup.find_all('figure'):
                gist_soup = fig.find('iframe', title=re.compile('.*\.py'))
                if gist_soup == None:
                    continue
                else:
                    gists.append(gist_soup)
            return len(gists)
        except:
            print("Couldn't get count of gists.") 


    def count_links(self, soup):
        try:
            links = []
            for a in soup.find('section').find_all('a'):
                link = a.get('href')
                if link != None:
                    links.append(link)
            return len(links)
        except:
            print("Couldn't get amount of links.") 

    def count_code_chunks(self, soup):
        try:
            return len(soup.find_all('pre'))
        except:
            print("Couldn't get amount of code chunks from article.")
    
    def scrape(self, soup, link:str):
        im_size = self.get_mean_size(soup)
        if im_size == None:
            im_size = (None, None)
        article_data = {
            "title": self.get_title(soup),
            "publication": self.get_publication(soup),
            "link": link,
            "author": self.get_author(soup),
            "followers": self.get_followers(soup),
            "reading_time": self.get_reading_time(soup),
            "n_words": self.count_words(soup),
            "pure_text": self.get_pure_text(soup),
            #"blockquotes": self.get_blockquotes(soup),
            "date": self.get_date(soup),
            "responses": self.get_responses(soup),
            "n_code_chunks": self.count_code_chunks(soup),
            "bold_text_count": self.bold_text_count(soup),
            "italic_text_count": self.italic_text_count(soup),
            "mean_image_width": im_size[0],
            "mean_image_height": im_size[1],
            "n_images": self.count_figures(soup),
            "n_lists": self.count_lists(soup),
            #"n_gists": self.count_gists(soup),
            "n_vids": self.count_vids(soup),
            "n_links": self.count_links(soup),
            "claps": self.get_claps(soup)
        }
            
        return(article_data)


    def get_pure_text_(self, link, options):
        page_url = link

        driver = webdriver.Edge(options=options)
        try:
            driver.get(page_url)
        except:
            print("Can't get pure text")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        return self.get_pure_text(soup=soup)

    def get_date_current_year_(self, link, options):
        page_url = link

        driver = webdriver.Edge(options=options)
        try:
            driver.get(page_url)
        except:
            print("Can't get date")
        time.sleep(0.2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        try:
            date_string = soup.find('p', class_=r"pw-published-date").text 
            return datetime.datetime.strptime(date_string, '%b %d').strftime(f'%d/%m/{datetime.date.today().year}')
        except:
            print("Couldn't get date from article.") 

    def get_date_(self, link, options):
        page_url = link

        driver = webdriver.Edge(options=options)
        try:
            driver.get(page_url)
        except:
            print("Can't get pure text")
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        return self.get_date(soup=soup)