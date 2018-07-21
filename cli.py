from app import app, db
from models import PocketEntry
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import exc
import click
import requests

url = 'https://getpocket.com/explore/trending'

@app.cli.command()
#@click.argument('name')
def get_articles():
    '''
        This script is meant to be run from cronjob and as such, this method will do most of the heavy lifting
    '''

    result = requests.get(url)
    soup = BeautifulSoup(result.content, "lxml")

    main_divs = soup.find_all("li", "item media_item")

    for div in main_divs:

        anchor = div.find("a", "item_link")

        article_id = anchor['data-id']

        #If a record already exists, skip it
        if PocketEntry.query.filter_by(article_id=article_id).first(): continue 

        link_url = anchor['data-saveurl']

        image_div = div.find('div', 'item_image')
        thumbnail_url = image_div['data-thumburl']

        content = div.find('div', 'item_content')
        content_domain = content.find('cite').find('a').text
        content_title = content.find('h3').find('a').text
        content_excerpt = content.find('p', 'excerpt').text

        created_date = datetime.now()
        write_to_db(article_id, link_url, thumbnail_url, content_domain, content_title, content_excerpt, created_date)

def write_to_db(article_id, url, thumbnail_url, content_domain, content_title, content_excerpt, created_date):

    #Takes a list of data and writes to database
    new_entry = PocketEntry(article_id=article_id,
            url=url,
            thumbnail_url=thumbnail_url,
            content_domain=content_domain,
            content_title=content_title,
            content_excerpt=content_excerpt,
            created_date=created_date)

    try:

        db.session.add(new_entry)
        db.session.commit()

    #I cannot actually get this to work without adding more packages seemingly because this exception cannot be caught until after a commit happens
    except exc.IntegrityError as error:
        db.session().rollback()
        print("ALREADY IN DB")
