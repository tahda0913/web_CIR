from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.CIR import bp
from app.CIR.forms import CIRForm
from app.CIR.email import CIR_mail
from flask_login import current_user, login_required
from app.models import User, CIReport, SchoolLookup

@bp.route('/CIR', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    return render_template("CIR/CIR.html", title="Critical Incident Report", form=form)

@bp.route('/user/report/<report_id>', methods=['GET', 'POST'])
@login_required
def CIR_review(report_id):
    form = CIRForm()
    if current_user.is_authenticated:
        report = CIReport.query.get(report_id)
        if form.validate_on_submit():
            report.incident_datetime = form.incident_date.data
            report.school_name = form.school_name.data
            report.incident_type = form.incident_type.data
            report.narrative = form.incident_narrative.data
            report.comments = form.comments.data
            report.phys_restraint = form.phys_restraint.data
            report.police = form.police.data
            report.phys_harm = form.phys_harm.data
            report.fire_rescue = form.fire_rescue.data
            report.dcyf = form.dcyf.data
            report.risk_assessment = form.risk_assessment.data
            report.cteam_response = form.cteam_response.data
            db.session.commit()
            CIR_mail(current_user, report)
            flash('Your changes have been saved.')
            return redirect(url_for('main.user', username=current_user.username))
        elif request.method == 'GET':
            form.incident_date.data = report.incident_datetime
            form.school_name.data = report.school_name
            form.incident_type.data = report.incident_type
            form.incident_narrative.data = report.narrative
            form.comments.data = report.comments
            form.phys_restraint.data = report.phys_restraint
            form.police.data = report.police
            form.phys_harm.data = report.phys_harm
            form.fire_rescue.data = report.fire_rescue
            form.dcyf.data = report.dcyf
            form.risk_assessment.data = report.risk_assessment
            form.cteam_response.data = report.cteam_response
        return render_template("CIR/edit_CIR.html", report=report, form=form)
    return redirect(url_for('auth.login'))
