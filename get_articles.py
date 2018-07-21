import requests
from bs4 import BeautifulSoup

url = 'https://getpocket.com/explore/trending'

def main():
    '''
        This script is meant to be run from cronjob and as such, this method will do most of the heavy lifting
    '''

    result = requests.get(url)
    soup = BeautifulSoup(result.content)

    main_divs = soup.find_all("li", "item media_item")

    for div in main_divs:

        anchor = div.find("a", "item_link")

        data_id = anchor['data-id']
        link_url = anchor['data-saveurl']

        image_div = div.find('div', 'item_image')
        thumbnail = image_div['data-thumburl']

        content = div.find('div', 'item_content')
        content_domain = content.find('cite').find('a').text
        content_title = content.find('h3').find('a').text
        content_excerpt = content.find('p', 'excerpt').text

        content_to_write = []
        content_to_write.append(data_id)
        content_to_write.append(link_url)
        content_to_write.append(thumbnail)
        content_to_write.append(str(content_domain))
        content_to_write.append(content_title)
        content_to_write.append(content_excerpt)

        write_to_db(content_to_write)

def write_to_db(content):
    '''
        Takes a list of data and writes to database
    '''
    print("#######################")
    print("#######################")
    print("#######################")
    print("#######################")
    print(content)

if __name__  == '__main__':
    main()
