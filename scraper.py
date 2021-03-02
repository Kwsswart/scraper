import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time


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


# variables for each scrape
max_results_per_area = 100
areas = ["Madrid+provincia", "Las+Palmas+provincia", "Galicia", "Barcelona+provincia", "Cádiz+provincia"]
columns = ["Area", "Job Title", "Company Name", "Location", "Summary", "Salary"]
df = pd.DataFrame(columns=columns)

# Scraping loop:
for area in areas:
    for start in range(0, max_results_per_area, 10):
        url = "http://es.indeed.com/jobs?q=Junior+developer&l=" + str(area) + "&jt=fulltime&lang=en&start=" + str(start)
        page = requests.get(url)
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
            df = df.append(job_post)

# save to csv
df.to_csv("sample.csv", sep='\t', encoding='utf-8')



