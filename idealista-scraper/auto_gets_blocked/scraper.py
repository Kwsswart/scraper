import csv
import json
import random
from call import Request
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options,DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException


def get_links(soup: object) -> list:
   '''
   Function to parse through url and extract the page urls to scrape
   '''

   links = []
   for sect in soup.find_all(name="section", attrs={"class": "items-container"}):
      for a in sect.find_all(name="a", attrs={"class": "item-link"}):
         links.append("https://www.idealista.com" + a["href"])
   if len(links) != 0:
      return links
   else: 
      main()
      

def find_information(soup: object, url: str) -> dict:
   '''
   Function to parse through each page individually and return dictionary
   '''
   try:
      for main in soup.find_all(name="main", attrs={"class": "detail-container"}):
         if main:
            url = url

            price = ''
            price_no = ''
            for span in main.find_all(name="span", attrs={"class":"info-data-price"}):
               price = span.text.strip()
               s = span.find("span")
               price_no = s.text
            if price == '':
               price = "Not Found"

            deposit = ''
            for span in main.find_all(name="span", attrs={"class", "txt-deposit"}):
               s = span.find("span")
               deposit = s.text
            if deposit == '':
               deposit = "Not Found"
            
            size = ''
            size_no = ''
            for div in main.find_all(name="div", attrs={"class", "info-features"}):
               span = div.find("span")
               size = span.text.strip()
               s = span.find("span")
               size_no = s.text 
            if size == '':
               size = "Not Found"
            
            message = ''
            for div in main.find_all(name="div", attrs={"class", "comment"}):
               p = div.find("p")
               message = p.text.strip()
            if message == '':
               message = "Not Found"

            features = []
            for div in main.find_all(name="div", attrs={"class","details-property-feature-one"}):
               d = div.find("div")
               for li in d.find_all(name="li"):
                  features.append(li.text.strip())

            building = []
            for div in main.find_all(name="div", attrs={"class", "details-property-feature-two"}):
               d = div.find("div")
               for li in d.find_all(name="li"):
                  building.append(li.text.strip())

            time = ''
            for p in main.find_all(name="p", attrs={"class","date-update-text"}):
               time = p.text.strip()
            if time == '':
               time = "Not Found"

            advertiser = ''
            for div in main.find_all(name="div", attrs={"class", "professional-name"}):
               advertiser = div.text.strip()
            if advertiser == '':
                  advertiser = "Not Found"

            phone = ''
            reference = ''
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

            location = []
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

            if size_no != '' and price_no != '':
               pricePerMeterSquared = round(int(final_p)/int(final_s), 2)
            else:
               pricePerMeterSquared = "Not Found"
         else:
            raise Exception('No main in page!')
   except:
      print("Problem")
      print(soup)
      browser = Request(url)
      page_html = browser.get_selenium_res("professional-name")
      soup = bs(page_html, "lxml")
      find_information(soup=soup, url=url)
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
   
def get_data(urls: list):
   '''
   Function to send requests based on the number of urls
   '''

   links = urls
   for i in range(39):
      try:
         print(i + 1)
         url = random.choice(links)
         browser = Request(url)
         page_html = browser.get_selenium_res("professional-name")
         soup = bs(page_html, "lxml")
         house = find_information(soup=soup, url=url)
         data.append(house)
         links.remove(url)
         print(house)
         sleep(random.randint(20,30)*10)
         driver.close()
      except TimeoutException:
         print("failed")
         return get_data(links)


def main():
   page_url = "https://www.idealista.com/alquiler-viviendas/madrid/centro/malasana-universidad/pagina-4.htm"

   link_page = Request(page_url)
   soup_file = link_page.get_selenium_res("footer-links-about")
   soup = bs(soup_file, "lxml")
   
   links = get_links(soup)
   data = []

   get_data(urls=links)
   json = json.dumps(data)

   with open("sample.json", "w") as json_output:
      json_output.write(json)

   with open("sample.txt", "w") as text_output:
      text_output.write(json)

   keys = data[0].keys()
   with open("sample.csv", "w", newline='')  as csv_output:
      dict_writer = csv.DictWriter(csv_output, keys)
      dict_writer.writeheader()
      dict_writer.writerows(data)

if __name__ == '__main__':
   main()
