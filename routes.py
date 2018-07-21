from flask import render_template, request
from app import app
from cli import get_articles
#from controllers import fetch_data_for_page, get_data_from_database, make_cache_key, fetch_data_for_several_pages

@app.route('/')
def index():
    
    #return render_template("index.html", page_number=page_number, results=github_entries, pages_available=pages_to_show_links_for)
    return 'Hello, World!'
