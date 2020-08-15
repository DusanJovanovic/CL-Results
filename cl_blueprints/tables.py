from flask import Blueprint, jsonify

from extensions import db
from models import Result

tables = Blueprint("tables", __name__)