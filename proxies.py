from lxml.html import fromstring
import requests
from itertools import cycle
import traceback


def get_proxies():
    """
    Function to fetch a set object of free proxies
    """
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):# grab only 10
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies
   

def test_proxies():
    proxies = get_proxies()
    proxy_pool = cycle(proxies)

    url = "https://httpbin.org/ip"

    for i in range(1,len(proxies)):
        proxy = next(proxy_pool)
        print("Request #%d"%i)
        try:
            response = requests.get(url,proxies={"http://": proxy, "https://": proxy})
            print(response.json())
        except:
            print("Skipping. ConnectionError")
