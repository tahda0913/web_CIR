from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    reports = db.relationship('CIReport', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class CIReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_inserted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    incident_datetime = db.Column(db.DateTime)
    school_name = db.Column(db.String(120), index=True)
    incident_type = db.Column(db.String(100), index=True)
    narrative = db.Column(db.Text)
    comments = db.Column(db.Text)
    phys_restraint = db.Column(db.Boolean)
    police = db.Column(db.Boolean)
    phys_harm = db.Column(db.Boolean)
    fire_rescue = db.Column(db.Boolean)
    dcyf = db.Column(db.Boolean)
    risk_assessment = db.Column(db.Boolean)
    cteam_response = db.Column(db.String(350))

    def __repr__(self):
        return f'CIR Num {self.id} authored by {self.author}'


class CIRStudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lasid = db.Column(db.Integer, index=True)
    student_race = db.Column(db.String(50))
    student_gender = db.Column(db.String(25))
    student_grade = db.Column(db.Integer)
    incident_role = db.Column(db.String(50))
    school_enrolled = db.Column(db.String(100), index=True)
    parent_notified = db.Column(db.Boolean)
    cir_id = db.Column(db.Integer, db.ForeignKey('ci_report.id'))
    incident = db.relationship('CIReport',
        backref=db.backref('students', lazy='dynamic', collection_class=list)
    )

    def __repr__(self):
        return f'Student {self.lasid} involved in CIR {self.cir_id}'



class SchoolLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200))
    dist_list = db.Column(db.String(600))

    def __repr__(self):
        return f'School: {self.school_name}'

def get_school_list():
    list = SchoolLookup.query.with_entities(SchoolLookup.school_name)
    return [sch_name for tuple in list for sch_name in tuple]


class IncidentLookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(120))

    def __repr__(self):
        return f'Incident: {self.incident_type}'

def get_incident_types():
    list = IncidentLookup.query.with_entities(IncidentLookup.incident_type)
    return [incident for tuple in list for incident in tuple]


class CrisisTeamResponses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.String(400))

    def __repr__(self):
        return f'Response: {self.response}'

def get_crisis_response():
    list = CrisisTeamResponses.query.with_entities(CrisisTeamResponses.response)
    return [response for tuple in list for response in tuple]
