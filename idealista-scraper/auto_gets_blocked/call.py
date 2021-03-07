import os
import zipfile
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager

import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from time import sleep

PROXY_HOST = 'proxy.scrapingdog.com'  # rotating proxy or host
PROXY_PORT = 8081 # port
PROXY_USER = 'scrapingdog' # username
PROXY_PASS = <api key> # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


class Request:
    '''
    Sets up selenium driver, proxy rotation, and user_rotation and sends request to url passed on instantation.
    '''
    
    selenium_retries = 0
    
    def __init__(self, url: str):
        self.url = url

    def get_selenium_res(self, class_name=None: str) -> object:
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value,
                                OperatingSystem.LINUX.value]

            user_agent_rotator = UserAgent(software_names=software_names,
                                        operating_systems=operating_systems,
                                        limit=100)
            user_agent = user_agent_rotator.get_random_user_agent()

            browser = self.get_chromedriver(use_proxy=True, user_agent=user_agent)

            # proxy testing
            #browser.get("http://lumtest.com/myip.json")
            browser.get(self.url)

            time_to_wait = 120 # add more
            sleep(20)
            try: 
                if class_name:
                    webDriverWait(browser, time_to_wait).until(
                        EC.presence_of_element_located((By.CLASS_NAME, class_name))
                    )
            finally:
                browser.maximize_window()
                page_html = browser.page_source
                browser.close()
                return page_html
        except (TimeoutException, WebDriverException):
            sleep(6)
            self.selenium_retries += 1
            print("retry")
            return self.get_selenium_res(class_name)

    def get_chromedriver(self,use_proxy=False: bool, user_agent=None: str) -> object:
        
        chrome_options = Options()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % user_agent)
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
            chrome_options=chrome_options)
        return driver