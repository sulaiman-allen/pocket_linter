import json
#from requests import get
#from flask import request
from models import PocketEntry
from app import db

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def get_data_from_database(page_number, results_per_page):
    '''
        Returns a page worth of results from database. Uses page_number for performing an offset.
    '''
    offset = (page_number - 1) * results_per_page

    return db.session.query(PocketEntry).order_by(PocketEntry.id.desc()).offset(offset).limit(results_per_page).all()

def get_number_of_pages_to_show(results_per_page):
    '''
        Returns the number of pages that should be shown at the bottom as available page links
    '''

    return int(PocketEntry.query.count() / results_per_page) if PocketEntry.query.count() % results_per_page == 0 else int(PocketEntry.query.count() / results_per_page) + 1
