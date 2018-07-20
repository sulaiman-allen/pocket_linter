'''
    Program for downloading trending articles on pocket.
'''
import requests
from bs4 import BeautifulSoup

url = 'https://getpocket.com/explore/trending'

def main():

    content = requests.get(url)
    soup = BeautifulSoup(content)




if __name__  == '__main__':
    main()
