from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, CIRForm
from app.email import CIR_mail
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, CIReport, SchoolLookup
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/CIR', methods=['GET', 'POST'])
@login_required
def CIR():
    form = CIRForm()
    if form.validate_on_submit():
        report = CIReport(
            author=current_user,
            incident_datetime=form.incident_date.data,
            school_name=form.school_name.data,
            incident_type=form.incident_type.data,
            narrative=form.incident_narrative.data,
            comments=form.comments.data,
            phys_restraint=form.phys_restraint.data,
            police=form.police.data,
            phys_harm=form.phys_harm.data,
            fire_rescue=form.fire_rescue.data,
            dcyf=form.dcyf.data,
            risk_assessment=form.risk_assessment.data,
            cteam_response=form.cteam_response.data
        )
        db.session.add(report)
        db.session.commit()
        CIR_mail(current_user, report)
        flash('Thank you for submitting your report')
        return redirect(url_for('index'))
    return render_template("CIR.html", title="Critical Incident Report", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    if current_user.is_authenticated:
        user = User.query.filter_by(username=username).first_or_404()
        reports = [report for report in user.reports]
        return render_template('user.html', user=user, reports=reports)
    return redirect(url_for('login'))

@app.route('/user/report/<report_id>')
@login_required
def CIR_review(report_id):
    if current_user.is_authenticated:
        report = CIReport.query.get(report_id)
        return render_template("view_CIR.html", report=report)
    return redirect(url_for('login'))