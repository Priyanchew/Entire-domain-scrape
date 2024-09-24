import pandas as pd
import csv
import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from path import util
from media import getMedia
from textfromsite import extract_bs4, create_multi_page_pdf

def loadRSS(url, filename):
    try:
        # creating HTTP response object from given url
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return

    # saving the xml file
    with open(filename, 'wb') as f:
        f.write(resp.content)


def parseXML(xmlfile):

    # Parse the XML file
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    # Define the namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    # Find all <loc> elements
    loc_elements = root.findall('.//ns:loc', namespace)

    # Extract the URLs from the <loc> elements
    urls = [loc.text for loc in loc_elements]

    return urls



def savetoexcel(urls, filename):
    df = pd.DataFrame(urls, columns=['URL'])
    df.to_excel(filename, index=False)


def main():
    url = input('Enter the company website: ')
    url = url + '/sitemap.xml'
    domain = urlparse(url).netloc
    # Remove www. and .com from domain
    downloadto = domain.replace('www.', '').replace('.com', '').replace('.org', '').replace('.in', '')

    # load rss from web to update existing xml file
    loadRSS(url, f'{downloadto}.xml')
    # parse xml file
    urls = ['https://www.nseindia.com/get-quotes/equity?symbol=MKPL']
    savetoexcel(urls, f'{downloadto}.xlsx')
    allText = []

    for url in urls:
        getMedia(url)
        text = extract_bs4(url)
        allText.append(text)
    path = os.path.join(downloadto,'ALLTEXT', 'ALLTEXT.pdf')
    if not os.path.exists(os.path.join(downloadto,'ALLTEXT')):
        os.makedirs(os.path.join(downloadto,'ALLTEXT'))
    create_multi_page_pdf(path, allText)


if __name__ == "__main__":
    main()

