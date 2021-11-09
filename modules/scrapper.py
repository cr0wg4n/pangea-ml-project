from bs4 import BeautifulSoup
import requests

def image_detector(url):
    _url = url.lower()
    if (".jpg" in _url or ".jpeg" in _url or ".png" in _url):
        return url
    return None

def get_page(url):
    headers = {
    }
    response = requests.get(url)
    html = response.content
    return html 

def get_data(url):
    soup = BeautifulSoup(get_page(url), 'html.parser')
    urls = soup.find_all("a", href=True)
    urls = [link["href"] for link in urls]
    images = soup.find_all('img', src=True) 
    images = [image["src"] for image in images if image_detector(image["src"])]
    paragraphs = soup.find_all('p')
    paragraphs = [paragraph.text for paragraph in paragraphs]
    return {
        "paragraphs": paragraphs,
        "urls": urls,
        "images": images
    }