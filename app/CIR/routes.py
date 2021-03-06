from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.CIR import bp
from app.CIR.forms import CIRForm, CIRStudentForm
from app.CIR.email import CIR_mail
from flask_login import current_user, login_required
from app.models import User, CIReport, SchoolLookup, CIRStudents

@bp.route('/CIR', methods=['GET', 'POST'])
@login_required
def CIR():
    cir = CIRForm()
    if cir.validate_on_submit():
        report = CIReport(
            author=current_user,
            incident_datetime=cir.incident_date.data,
            school_name=cir.school_name.data,
            incident_type=cir.incident_type.data,
            narrative=cir.incident_narrative.data,
            comments=cir.comments.data,
            phys_restraint=cir.phys_restraint.data,
            police=cir.police.data,
            phys_harm=cir.phys_harm.data,
            fire_rescue=cir.fire_rescue.data,
            dcyf=cir.dcyf.data,
            risk_assessment=cir.risk_assessment.data,
            cteam_response=cir.cteam_response.data
        )
        db.session.add(report)

        for student in cir.students.data:
            new_student = CIRStudents(**student)
            report.students.append(new_student)

        db.session.commit()
        CIR_mail(current_user, report)
        flash('Thank you for submitting your report')
        return redirect(url_for('main.index'))
    return render_template("CIR/CIR.html", title="Critical Incident Report", cir=cir)

@bp.route('/user/report/<report_id>', methods=['GET', 'PUT'])
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
