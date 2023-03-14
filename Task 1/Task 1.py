import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.visited_html = []
        self.urls_to_visit = urls

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
      if (len(self.urls_to_visit) < 100):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)
            myFile=open('/content/urls.txt', 'w')
            myFile.write(str(url) + '\n')
            myFile.close()

    def crawl(self, url):
        html = self.download_url(url)
        print('HTML')
        self.visited_html.append(html)
        for url in self.get_linked_urls(url, html):
            if (len(self.urls_to_visit) < 100):
              self.add_url_to_visit(url)
            else:
              break  

    def run(self):
        while len(self.urls_to_visit) < 100:
          if (len(self.urls_to_visit) > 0):
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            print(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                print(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)
                print('end: ' + str(len(self.urls_to_visit)))
                for i in range(len(self.urls_to_visit)):
                  if (self.urls_to_visit[i] != None):
                    if (len(self.visited_html) < 100):
                     self.visited_html.append(self.download_url(self.urls_to_visit[i]))
                     print('html: ' + str(len(self.visited_html)))
                print(str(len(self.visited_html)))
                i = 0
                for element in self.visited_html:
                   myFile=open(str(i) + '.txt', 'w')
                   i = i + 1
                   print(element.index)
                   myFile.write(element)
                   myFile.write('\n')
                   myFile.close()

Crawler(urls=['https://habr.com/ru/all/']).run()