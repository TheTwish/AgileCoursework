from flask import Blueprint, render_template, redirect, url_for, request
from flask_paginate import Pagination, get_page_args
from app.models import User, Event

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
@main.route('/index/<cat>', methods=['GET', 'POST'])
def index(cat=None):
    page = int(request.args.get('page', 1))
    per_page = 8
    offset = (page - 1) * per_page

    events = Event.query.order_by(Event.name.asc())
    #categories = [cat.name for cat in Category.query.all()]
    #if cat is not None:
        #books = [b.books.order_by(Book.title.asc()) for b in Category.query.filter_by(name=cat)][0]

    events_for_render = events.limit(per_page).offset(offset)
    search =False
    q = request.args.get('q')
    if q:
        search=True
    pagination = Pagination(
        page=page, 
        per_page=per_page,
        offset=offset,
        total=events.count(),
        css_framework='bootstrap3',
        search=search
        )

    return render_template('index.html', events=events_for_render,
    pagination=pagination, title='Home')