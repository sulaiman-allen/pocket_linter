from flask import render_template, request
from app import app, db
from cli import get_articles
from controllers import get_data_from_database, get_number_of_pages_to_show

RESULTS_PER_PAGE = 24

@app.route('/')
def index():
    '''
        Main page
    '''

    page_number = int(request.args.get('page_num')) if request.args.get('page_num') else 1

    return render_template("index.html",
                           page_number=page_number,
                           results=get_data_from_database(page_number, results_per_page=RESULTS_PER_PAGE), # Load freshly downloaded information from database
                           pages_available=get_number_of_pages_to_show(RESULTS_PER_PAGE)) # Get the total number of pages available to show links for
