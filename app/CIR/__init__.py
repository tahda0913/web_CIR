from flask import Blueprint

bp = Blueprint('CIR', __name__)

from app.CIR import routes, forms, email
