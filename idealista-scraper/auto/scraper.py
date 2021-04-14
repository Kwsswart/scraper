import csv
import json
import random
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options,DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:

    def __init__(self, listings_url: str):
        self.links = self.get_links(listings_url)
        self.data = []


    def get_links(self, url: str) -> list:
        '''
        Function to parse through url and extract the page urls to scrape
        '''

        opts = Options()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        soup_file=driver.page_source
        soup = bs(soup_file, "lxml")
        driver.close()
        links = []
        for sect in soup.find_all(name="section", attrs={"class": "items-container"}):
            for a in sect.find_all(name="a", attrs={"class": "item-link"}):
                links.append("https://www.idealista.com" + a["href"])
                
        return links

    def get_page(self):
        '''
        Function to get each page as requested
        '''

        if len(self.links) == 0:
            print("No links left")
            return
        url = random.choice(self.links)
        self.links.remove(url)
        print(len(self.links))
        opts = Options()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        soup_file=driver.page_source
        soup = bs(soup_file, "lxml")

        d = self.find_information(soup, url)
        driver.close()
        print(d)
        self.data.append(d)

    def find_information(self, soup: object, url: str) -> dict:
        '''
        Function to parse through each page individually and return dictionary
        '''
        url = url
        price = ''
        price_no = ''
        deposit = ''         
        size = ''
        size_no = ''
        message = ''
        features = []
        building = []
        time = ''
        advertiser = ''
        phone = ''
        reference = ''
        pricePerMeterSquared = ''
        location = []
        
        try:
            for main in soup.find_all(name="main", attrs={"class": "detail-container"}):
                for span in main.find_all(name="span", attrs={"class":"info-data-price"}):
                    price = span.text.strip()
                    s = span.find("span")
                    price_no = s.text
                if price == '':
                    price = "Not Found"

                for span in main.find_all(name="span", attrs={"class", "txt-deposit"}):
                    s = span.find("span")
                    deposit = s.text
                if deposit == '':
                    deposit = "Not Found"

                for div in main.find_all(name="div", attrs={"class", "info-features"}):
                    span = div.find("span")
                    size = span.text.strip()
                    s = span.find("span")
                    size_no = s.text 
                if size == '':
                    size = "Not Found"
                
                for div in main.find_all(name="div", attrs={"class", "comment"}):
                    p = div.find("p")
                    message = p.text.strip()
                if message == '':
                    message = "Not Found"

                for div in main.find_all(name="div", attrs={"class","details-property-feature-one"}):
                    d = div.find("div")
                    for li in d.find_all(name="li"):
                        features.append(li.text.strip())

                for div in main.find_all(name="div", attrs={"class", "details-property-feature-two"}):
                    d = div.find("div")
                    for li in d.find_all(name="li"):
                        building.append(li.text.strip())

                for p in main.find_all(name="p", attrs={"class","date-update-text"}):
                    time = p.text.strip()
                if time == '':
                    time = "Not Found"

                for div in main.find_all(name="div", attrs={"class", "professional-name"}):
                    advertiser = div.text.strip()
                if advertiser == '':
                    advertiser = "Not Found"

                for div in main.find_all(name="div", attrs={"class", "advertiser-data"}):
                    for d in div.find_all(name="div", attrs={"class", "last-phone"}):
                        p = d.find("p")
                        phone = p.text.strip()
                    for p in div.find_all(name="p", attrs={"class": "txt-ref"}):
                        reference = p.text.strip()
                if phone == '':
                    phone = "Not Found"
                if reference == '':
                    reference = "Not Found"

                for div in main.find_all(name="div", attrs={"id": "mapWrapper"}):
                    ul = div.find("ul")
                    for li in ul.find_all(name="li"):
                        location.append(li.text.strip())

                if price_no != '':
                    p = list(price_no)
                    for i in range(len(p) - 1):
                        if not p[i].isdigit():
                            p.remove(p[i])
                    final_p = "".join(p)

                if size_no != '':
                    s = list(size_no)
                    for i in range(len(s) - 1):
                        if not s[i].isdigit():
                            s.remove(s[i])
                    final_s = "".join(s)

                if size_no != '' and size_no != '':
                    pricePerMeterSquared = round(int(final_p)/int(final_s), 2)
                else:
                    pricePerMeterSquared = "Not Found"
        except:
            print("Problem")
        return {
                "idealistaUrl": url,
                "precio": price,
                "fianca": deposit,
                "tamano": size,
                "precioPorMetroCuadrdo": pricePerMeterSquared,
                "localidad": location,
                "mensaje": message,
                "caracteristicas": features,
                "caracterisricasEdificio": building,
                "anunciante": advertiser,
                "movil": phone,
                "referencia": reference,
                "ultimaActualizacion": time
            }
    
    def to_json(self):
        '''
        Save data to json
        '''

        js = json.dumps(self.data)
        with open("sample.json", "w") as json_output:
            json_output.write(js)

    def to_csv(self):
        '''
        Save data to csv file
        '''

        keys = self.data[0].keys()
        with open("sample.csv", "w", newline='')  as csv_output:
            dict_writer = csv.DictWriter(csv_output, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.data)

    def to_text(self):
        '''
        Save data to text
        '''

        js = json.dumps(self.data)
        with open("sample.txt", "w") as text_output:
            text_output.write(js)