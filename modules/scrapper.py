from bs4 import BeautifulSoup
import requests

def image_detector(url):
    _url = url.lower()
    if (".jpg" in _url or ".jpeg" in _url or ".png" in _url):
        return url
    return None

def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (BeOS; U; BeOS BePC; en-US; rv:1.8.1b2) Gecko/20060901 Firefox/2.0b2'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if (response.status_code == 200):
            html = response.content
            return html 
        return None
    except Exception as error: 
        print(error)
        return None

def get_data(url):
    html = get_page(url)
    if (html):
        soup = BeautifulSoup(html, 'html.parser')
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
    return None