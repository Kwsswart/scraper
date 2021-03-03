import csv 
import bs4 
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from proxy import Proxies


class Amazon_Scraper:

    def __init__(self, search_word, max_search_results, language):
        self.search_word = self.format_search_word(word=search_word)
        self.max_pages = int(round(max_search_results/18))
        self.language = language

    def format_search_word(self, word):
        w = list(word)
        for i in range(len(w) - 1):
            if w[i] == ' ':
                w[i] == '+'
        return "".join(w)

    def extract_name(self, div):
        name = ''
        for h in div.find_all(name="h2"):
            for a in h.find_all(name="a"):
                for s in a.find_all(name="span"):
                        name = s.text
        return name

    def extract_rating(self, div):
        rating = ''
        for a in div.find_all(name="a", attrs={"class":"a-popover-trigger"}):
            for s in a.find_all(name="span"):
                rating = s.text
        return rating

    def extract_image_link(self, div):
        image_link = ''
        for sp in div.find_all(name="span", attrs={"data-component-type":"s-product-image"}):
            for i in sp.find_all(name="img"):
                image_link = i["src"]
        return image_link

    def extract_price(self, div):
        price = ''
        for sym in div.find_all(name="span", attrs={"class":"a-price-symbol"}):
            price = price + sym.text + ' '
        for sym in div.find_all(name="span", attrs={"class":"a-price-whole"}):
            price = price + sym.text
        for sym in div.find_all(name="span", attrs={"class":"a-price-fraction"}):
            price = price + sym.text
        return price

    def scrape(self):

        prox = Proxies()
        columns = ["Description", "Rating", "Price", "Image"]
        df = pd.DataFrame(columns=columns)

        for start in range(0, self.max_pages):
            print(start)
            proxy = prox.return_proxy()
            URL = "https://www.amazon.com/s?k=" + str(self.search_word) + "&page=" + str(start) + "&language=" + str(self.language)
            try:
                page = requests.get(URL,proxies={"http://": proxy, "https://": proxy}, headers=prox.return_header())
                time.sleep(15)
                soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
                for div in soup.find_all(name="div", attrs={"class": "s-result-item"}):
                    num = (len(df) + 1)
                    product = []
                    product.append(self.extract_name(div))
                    if product[0] == '':
                        continue
                    product.append(self.extract_rating(div))
                    product.append(self.extract_price(div))
                    product.append(self.extract_image_link(div))
                    df.loc[num] = product
            except:
                print("There was a problem")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
            print(df)
        
        df.to_csv("sample.csv", quoting=csv.QUOTE_ALL, encoding="utf-8")

