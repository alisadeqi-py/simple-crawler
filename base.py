from abc import ABC , abstractclassmethod
import requests
from bs4 import BeautifulSoup
import json
from conf import BASE_LINK



class CrawlerBase(ABC):

    @abstractclassmethod
    def start(self):
        pass
    
    @abstractclassmethod
    def start(self , data):
        pass


class LinkCrawler(CrawlerBase):

    def __init__(self , cities , link=BASE_LINK):
        self.cities = cities
        self.link = link


    def get_page(self , link):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text)
            res_2 = soup.find('span' , attrs={'class' : 'totalcount'})
            response_2 = requests.get(link + res_2.string)    
        except:
            return None
        return response_2

    def find_links(self , html_doc):
        soup = BeautifulSoup(html_doc)
        res = soup.find_all( 'a' , attrs = {'class' : 'result-title hdrlnk'} )
        return res

    def start(self , link):
        start =  0 
        crawl = True 
        adv_link = []
        response = self.get_page(link)
        new_links = self.find_links(response.text)
        adv_link.extend(new_links)
        return adv_link

    
    def start_crawl(self):
        adv_links = []
        for city in self.cities:
            links = self.start(self.link.format(city))
            print( city , 
            len(links))
            adv_links.extend(links)
        self.store([li.get('href') for li in adv_links])
    def store(self , data):
        with open('data/data.json' , 'w') as f:
            f.write(json.dumps(data))

class DataCrawler(CrawlerBase):
    pass  