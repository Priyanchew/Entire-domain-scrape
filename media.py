import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def create_directory(directory, path):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(os.path.join(directory, path))
        else:
            os.makedirs(os.path.join(directory, path))
    except Exception as e:
        print(f'Failed to create directory {directory}: {e}')


def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')
    except IOError as e:
        print(f'Failed to write file {save_path}: {e}')


def get_media_files(url):
    media_links = set()
    try:
        response = requests.get(url)
        print(response.raise_for_status())
        soup = BeautifulSoup(response.content, 'html.parser')

        # Define the file extensions you want to download
        media_extensions = ['.pdf', '.xlsx', '.docx', '.pptx', '.csv', '.xml']

        # Extract all media file links
        for ext in media_extensions:
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                if href.lower().endswith(ext):
                    media_links.add(urljoin(url, href))

            for tag in soup.find_all('img', src=True):
                src = tag['src']
                if src.lower().endswith(ext):
                    media_links.add(urljoin(url, src))

            for tag in soup.find_all('source', src=True):
                src = tag['src']
                if src.lower().endswith(ext):
                    media_links.add(urljoin(url, src))

    except requests.RequestException as e:
        print(f'Failed to fetch the webpage {url}: {e}')
    return media_links


def getMedia(url):
    try:
        domain = urlparse(url).netloc
        path = urlparse(url).path[1:].replace('.html', '')
        # Remove www. and .com from domain
        download_folder = domain.replace('www.', '').replace('.com', '').replace('.org', '').replace('.in', '')
        # Create download directory if it doesn't exist
        create_directory(download_folder, path)

        # Get all media file links
        media_links = get_media_files(url)

        # Download each media file
        for media_link in media_links:
            parsed_url = urlparse(media_link)
            file_name = os.path.basename(parsed_url.path)
            save_path = os.path.join(download_folder, path, file_name)
            download_file(media_link, save_path)

    except Exception as e:
        print(f'An error occurred: {e}')

getMedia('https://www.nseindia.com/get-quotes/equity?symbol=MKPL')