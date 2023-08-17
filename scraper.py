import requests
import lxml
from bs4 import BeautifulSoup

#TODO: rewrite to use the list of URLs generated by crawler.py, in order to scrape and look for a specific result.

url = "https://www.google.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
}
f = requests.get(url, headers = headers)

soup = BeautifulSoup(f.content, 'lxml')

data = soup.find_all()

data_str = str(data)

with open('data.txt', 'w') as f:
    f.write(data_str)