import logging # Import logging module to log messages to a file
from urllib.parse import urljoin # Import urljoin function to join a base URL with a relative URL
import requests # Import requests module to make HTTP requests to web servers and download web pages
from bs4 import BeautifulSoup # Import BeautifulSoup module to parse HTML and extract links from web pages

# Configure logging to write messages to a file
logging.basicConfig(
    filename='crawl list', # Set the log file name
    filemode='a', # Append new messages to the log file
    format='%(asctime)s %(levelname)s:%(message)s', # Set the format for log messages
    level = logging.INFO # Set the logging level to INFO
)

# Define a class to encapsulate the crawling logic
class Crawler:

    # Initialize the class with a list of URLs to visit
    def __init__(self, urls=[]):
        self.visited_urls = [] # List to track visited URLs
        self.urls_to_visit = urls # List to track URLs to visit

    # Download the HTML content for a given URL
    def download_url(self, url):
        return requests.get(url).text

    # Parse the HTML content for a given URL and return any linked URLs
    def get_linked_urls(self,url,html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path =urljoin(url,path)
            yield path

    # Add a new URL to the list of URLs to visit
    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    # Crawl a given URL, downloading the HTML and extracting any linked URLs
    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    # Run the crawler, visiting each URL in the list of URLs to visit
    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0) # Get the next URL to visit
            logging.info(f'Crawling: {url}') # Log a message indicating that the crawler is visiting the URL
            try:
                self.crawl(url) # Crawl the URL and extract any linked URLs
            except Exception:
                #logging.exception(f'Failed to crawl: {url}')
                logging.raiseExceptions = False # If an error occurs, log a message but continue crawling
            finally:
                self.visited_urls.append(url) # Add the URL to the list of visited URLs

# Define the entry point for the script
if __name__ == '__main__':
    # Create a new Crawler object and run it with a starting URL
    Crawler(urls=['https://www.blaynewesneski.com']).run()
