from threading import Thread
from flask_mail import Message
from app import mail
from app import app
from app.models import User, CIReport, SchoolLookup

def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def CIR_mail(user, report):
    mail_subj = f'** ATTENTION CIR - {report.incident_datetime} {report.school_name} {report.incident_type}'
    sender = app.config['ADMINS'][0]
    school = SchoolLookup.query.filter_by(school_name=f'{report.school_name}').first()
    recipients = school.dist_list.split()
    author = User.query.filter_by(id=f'{report.author.id}').first()
    body = f"""
    Incident Date and Time: {report.incident_datetime}

    Writer's Name: {author.username}

    School: {report.school_name}

    Incident Type: {report.incident_type}

    Narrative: {report.narrative}

    Additional Comments: {report.comments}

    Police: {'Yes' if report.police else 'No'}

    Physical Harm: {'Yes' if report.phys_harm else 'No'}

    Fire/Rescue: {'Yes' if report.fire_rescue else 'No'}

    DCYF: {'Yes' if report.dcyf else 'No'}

    Physical Restraint Used: {'Yes' if report.phys_restraint else 'No'}

    Suicide Risk Assessment Administered: {'Yes' if report.risk_assessment else 'No'}

    Crisis Team Response for Suicidal Ideation: {report.cteam_response}
    """

    msg = Message(mail_subj, sender=sender, recipients=recipients, body=body)
    Thread(target=send_async_mail, args=(app, msg)).start()
