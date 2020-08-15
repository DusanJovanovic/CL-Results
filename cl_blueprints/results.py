from flask import Blueprint, jsonify

from extensions import db
from models import Result

results = Blueprint("results", __name__)


@results.route('/')
def hello_world():
    return 'Hello, World!'
