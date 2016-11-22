from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from datetime import datetime
import requests

ff_profile = webdriver.FirefoxProfile()
profile=ff_profile#webdriver.FirefoxProfile("/Users/laveeshrohra/Library/Application Support/TorBrowser-Data/Browser/kv9dcr1l.default")
binary = FirefoxBinary('/Applications/TorBrowser.app/Contents/MacOS/firefox')
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
browser=webdriver.Firefox(profile)
browser.get("http://icanhazip.com")
soup = BeautifulSoup(browser.page_source, "html.parser")
ip = soup.get_text().strip()
#print ip

start_time = datetime.now()
while True:
    resp = requests.get("http://icanhazip.com")
    soup = BeautifulSoup(browser.content, "html.parser")
    if ip != soup.get_text().strip():
        print ip
        print soup.get_text().strip()
        diff = datetime.now() - start_time
        print divmod(diff.days * 86400 + diff.seconds, 60)
        break

browser.save_screenshot("/Users/laveeshrohra/Downloads/screenshot2.png")

browser.close()