from modules.search import search
from modules.scrapper import get_data
import unittest

class Global(unittest.TestCase):
    def test_search(self):
        response = search("¿Qué lugar visitar en La Paz?")
        print(response)
        
    def test_scrapping(self):
        response = get_data("https://www.caminitoamor.com/la-paz-bolivia/")
        print(response)

if __name__ == '__main__':
    unittest.main()