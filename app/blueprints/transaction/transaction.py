from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from data_models import Customer  # Make sure this import is correct
from utils import role_required

trs = Blueprint('trs', __name__, template_folder="templates")

@trs.route('/')