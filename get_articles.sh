#!/bin/sh

export ENV FLASK_APP=/usr/src/pocket_linter/routes.py
flask get_articles
