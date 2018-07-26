from flask import render_template, request
from app import app, db
from cli import get_articles
from controllers import get_data_from_database, get_number_of_pages_to_show
from models import PocketEntry

RESULTS_PER_PAGE = 24

@app.route('/')
def index():
    
    page_number = int(request.args.get('page_num')) if request.args.get('page_num') else 1

    #load freshly downloaded information from database
    pocket_entries = get_data_from_database(page_number, results_per_page=RESULTS_PER_PAGE)
    pages_to_show_links_for = get_number_of_pages_to_show(RESULTS_PER_PAGE)

    return render_template("index.html", page_number=page_number, results=pocket_entries, pages_available=pages_to_show_links_for)
