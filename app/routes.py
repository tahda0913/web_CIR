from flask import render_template, url_for, flash, redirect, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    reports = user.reports.paginate(page, 10, False)
    next_url = url_for('user', username=user.username, page=reports.next_num) \
        if reports.has_next else None
    prev_url = url_for('user', username=user.username, page=reports.prev_num) \
        if reports.has_prev else None
    return render_template('user.html', user=user, reports=reports.items,
                            next_url=next_url, prev_url=prev_url)
