from lxml.html import fromstring
import requests
import random
from itertools import cycle
import traceback


def get_proxies() -> set:
    """
    Function to fetch a set object of free proxies
    """
    
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

referers = [
        "https://duckduckgo.com/",
        "https://www.google.com/",
        "http://www.bing.com/",
        "https://in.yahoo.com/",
        "https://www.azlyrics.com/",
        "https://www.dogpile.com/",
        "http://www.yippy.com",
        "https://yandex.com/"]

user_agents = [
    'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/windows/2',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/linux/',
	'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
	'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/chrome-os/',
	'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/mobile/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_platform_string/redmi/',
	'https://developers.whatismybrowser.com/useragents/explore/software_name/instagram/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/android/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/ios/',
	'https://developers.whatismybrowser.com/useragents/explore/operating_system_name/mac-os-x/'
]

class Proxies:

    def __init__(self, proxy_function=get_proxies, user_agents=user_agents: list, referers=referers: list):
        self.proxies = list(proxy_function())
        self.user_agents = user_agents
        self.referers = referers


    def return_header(self) -> dict:
        header = {
            'user-agent': self.user_agents[random.randint(0, len(self.user_agents)-1)],
            'referer': self.referers[random.randint(0, len(self.referers)-1)],
        }
        return header

    def return_proxy(self) -> list: 
        return self.proxies[random.randint(0, len(self.proxies)-1)]