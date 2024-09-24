import requests
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def extract_bs4(url):
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from common content tags
    main_content = []
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span', 'li', 'table', 'td', 'th', 'tr', 'tbody']:
        for element in soup.find_all(tag):
            main_content.append(element.get_text(strip=True))

    # Join all extracted text
    main_text = ' '.join(main_content)

    return main_text


def create_multi_page_pdf(filename, content_list):
    c = canvas.Canvas(filename, pagesize=letter)

    for content in content_list:
        c.setFont("Helvetica", 12)
        text_object = c.beginText(100, 750)

        # Split content into lines and add them to the text object
        for line in content.split('\n'):
            text_object.textLine(line)

        c.drawText(text_object)
        c.showPage()  # Move to a new page

    c.save()


alltext = extract_bs4('https://www.nseindia.com/get-quotes/equity?symbol=MKPL')
create_multi_page_pdf(os.path.join('nseindia', 'ALLTEXT.pdf'), [alltext])
