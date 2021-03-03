import requests
import bs4
from bs4 import BeautifulSoup
from proxies import get_proxies
from itertools import cycle
import pandas as pd
import time
import csv


def extract_title_from_result(soup):
    jobs =[]
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return jobs

def extract_company_from_result(soup):
    companies =[]
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            try_again = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in try_again:
                companies.append(span.text.strip())
    return companies

def extract_location_from_result(soup):
    locations = []
    spans = soup.find_all(name="span", attrs={"class":"location"})
    for span in spans:
        locations.append(span.text)
    return locations

def extract_salary_from_result(soup):
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            span = div.find(name="span", attrs={"class":"salary"})
            salaries.append(span.text.strip())
        except:
            salaries.append("Nothing Found")
    return salaries

def extract_summary_from_result(soup):
    summaries = []
    divs = soup.find_all(name="div", attrs={"class": "summary"})
    for div in divs:
        summaries.append(div.text.strip())
    return summaries


def scraper():
    # variables for each scrape
    HEADERS = ({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    })
    max_results_per_area = 100
    areas = ["Madrid+provincia", "Las+Palmas+provincia", "Galicia", "Barcelona+provincia", "Cádiz+provincia"]
    columns = ["Area", "Job Title", "Company Name", "Location", "Summary", "Salary"]
    df = pd.DataFrame(columns=columns)

    # Scraping loop:

    proxies = get_proxies()
    proxy_pool = cycle(proxies)

    for area in areas:
        for start in range(0, max_results_per_area, 10):
            print("*")
            proxy = next(proxy_pool)
            url = "http://es.indeed.com/jobs?q=Junior+developer&l=" + str(area) + "&jt=fulltime&lang=en&start=" + str(start)
            try:
                page = requests.get(url,proxies={"http://": proxy, "https://": proxy}, headers=HEADERS)
                time.sleep(15) # separate page grabs
                soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
                for div in soup.find_all(name="div", attrs={"class":"row"}):
                    num = (len(df) + 1) 
                    job_post = [] 
                    job_post.append(area)
                    # Title
                    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                        job_post.append(a["title"])
                    # Company Name
                    company = div.find_all(name="span", attrs={"class":"company"})
                    if len(company) > 0:
                        for b in company:
                            job_post.append(b.text.strip())
                    else:
                        try_again = div.find_all(name="span", attrs={"class":"result-link-source"})
                        for span in try_again:
                            job_post.append(span.text.strip())
                    # Location
                    spans = div.find_all(name="span", attrs={"class":"location"})
                    for span in spans:
                        job_post.append(span.text)
                    # Summary
                    dv = div.find_all(name="div", attrs={"class":"summary"})
                    for d in dv:
                        job_post.append(d.text.strip())
                    # Salary
                    try:
                        span = div.find(name="span", attrs={"class":"salary"})
                        job_post.append(span.text.strip())
                    except:
                        job_post.append("Nothing Found")
                    # Pass to pandas
                    df.loc[num] = job_post
            except:
                proxy = next(proxy_pool)
                page = requests.get(url,proxies={"http://": proxy, "https://": proxy})
                time.sleep(15) # separate page grabs
                soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
                for div in soup.find_all(name="div", attrs={"class":"row"}):
                    num = len(df) + 1 
                    job_post = [] 
                    job_post.append(area)
                    # Title
                    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
                        job_post.append(a["title"])
                    # Company Name
                    company = div.find_all(name="span", attrs={"class":"company"})
                    if len(company) > 0:
                        for b in company:
                            job_post.append(b.text.strip())
                    else:
                        try_again = div.find_all(name="span", attrs={"class":"result-link-source"})
                        for span in try_again:
                            job_post.append(span.text.strip())
                    # Location
                    spans = div.find_all(name="span", attrs={"class":"location"})
                    for span in spans:
                        job_post.append(span.text)
                    # Summary
                    dv = div.find_all(name="div", attrs={"class":"summary"})
                    for d in dv:
                        job_post.append(d.text.strip())
                    # Salary
                    try:
                        span = div.find(name="span", attrs={"class":"salary"})
                        job_post.append(span.text.strip())
                    except:
                        job_post.append("Nothing Found")
                    # Pass to pandas
                    df.loc[num] = job_post
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
    # save to csv
    df.to_csv("sample.csv",quoting=csv.QUOTE_ALL, encoding='utf-8')

scraper()