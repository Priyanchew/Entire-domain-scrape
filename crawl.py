import logging
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import re
import validators
from PyPDF2 import PdfReader
import keyboard

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

countforpdf = 0

def download_and_extract_pdf(pdf_url):
    global countforpdf
    # Download the PDF file
    response = requests.get(pdf_url)
    with open(f'downloaded_pdf{countforpdf}.pdf', 'wb') as file:
        file.write(response.content)

    # Extract text from the downloaded PDF
    with open(f'downloaded_pdf{countforpdf}.pdf', 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = reader.pages[3]
            text += page.extract_text()
        return text


def pathwithword(word, url):
    urlwithword = []
    for urls in url:
        path = urlparse(urls).path
        if word in path.lower():
            urlwithword.append(urls)
    return urlwithword


def is_pdf(link):
    return re.search(r'\.pdf$', link, re.IGNORECASE)


class Crawler:

    def __init__(self, urls=[]):
        self.main_url = urlparse(urls[0]).netloc
        self.visited_urls = set()
        self.urls_to_visit = set(urls)


    def download_url(self, url):
        return requests.get(url).text

    def is_valid_url(self, url):
        return validators.url(url)

    def is_same_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.main_url

    def printmainurl(self):
        print(self.main_url)

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if is_pdf(url):
            self.visited_urls.add(url)
        if url not in self.visited_urls and url not in self.urls_to_visit and self.is_valid_url(
                url) and not is_pdf(url) and url is not None and self.is_same_domain(url):
            self.urls_to_visit.add(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop()
            logging.info(f'Crawling: {url}')
            if keyboard.is_pressed('q'):
                print("Key 'q' pressed. Exiting loop.")
                break
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.add(url)
        return self.visited_urls


if __name__ == '__main__':
    sites = Crawler(urls=['https://www.tatasteel.com/']).run()
    for site in sites:
        print(site)
    while True:
        word = input("Enter words or type exit to quit: ")
        if word == 'exit':
            break
        else:
            linkswithword = pathwithword(word, sites)
            print(linkswithword if sites else 'No sites with that word found.')
            for url in linkswithword:
                if not is_pdf(url):
                    page_response = requests.get(url)
                    page_content = page_response.content
                    soup = BeautifulSoup(page_content, 'html.parser')

                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        print(p.get_text() if p.get_text() is not None else 'No text found in paragraph')

                else:
                    text = download_and_extract_pdf(url)
