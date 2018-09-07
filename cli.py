from datetime import datetime
from app import application, db
from models import PocketEntry
from bs4 import BeautifulSoup
from sqlalchemy import exc
#import click
import requests

URL = 'https://getpocket.com/explore/trending'

@application.cli.command()
#@click.argument('name')
def get_articles():
    '''
        This script is meant to be run from cronjob and as such, this method will do most of the heavy lifting
    '''

    result = requests.get(URL)
    soup = BeautifulSoup(result.content, "html.parser")

    card_list = []
    main_divs = soup.find_all("li", "media_item")

    # Go through all list items and scrape relevant information
    for div in main_divs:

        card_dict = {}
        card_dict['article_id']                     = div.find("a", "item_link")['data-id']

        #If a record already exists, skip it
        if PocketEntry.query.filter_by(article_id=card_dict['article_id']).first(): continue

        card_dict['link_url']                       = div.find("a", "item_link")['data-saveurl']
        card_dict['thumbnail_url']                  = div.find('div', 'item_image')['data-thumburl']
        card_dict['content_domain']                 = div.find('div', 'item_content').find('cite').find('a').text
        card_dict['content_date_published']         = div.find('div', 'item_content').find('cite').find('span', 'read_time').text
        card_dict['content_title']                  = div.find('div', 'item_content').find('h3').find('a').text
        card_dict['content_excerpt']                = div.find('div', 'item_content').find('p', 'excerpt').text
        card_dict['created_date']                   = datetime.now()
        card_list.append(card_dict)

    # Reverse order of articles as they were added. The most recent articles are being read in first, but they need to be saved as entries to the database backwards creating a stack instead
    # of a queue in order to save/show up in the right order.
    for article in reversed(card_list):
        write_to_db(article['article_id'], article['link_url'], article['thumbnail_url'], article['content_domain'], article['content_date_published'],
                    article['content_title'], article['content_excerpt'], article['created_date'])


def write_to_db(article_id, url, thumbnail_url, content_domain, content_date_published, content_title, content_excerpt, created_date):
    '''
        Takes a list of data and writes to database
    '''

    new_entry = PocketEntry(article_id=article_id,
                            url=url,
                            thumbnail_url=thumbnail_url,
                            content_date_published=content_date_published,
                            content_domain=content_domain,
                            content_title=content_title,
                            content_excerpt=content_excerpt,
                            created_date=created_date)

    try:
        db.session.add(new_entry)
        db.session.commit()
        print("[+] New Entry Added")

    #I cannot actually get this to work without adding more packages seemingly because this exception cannot be caught until after a commit happens
    except exc.IntegrityError as error:
        db.session().rollback()
        print("[+] Already In DB")
