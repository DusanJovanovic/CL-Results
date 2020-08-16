from flask import Blueprint, jsonify, request

from extensions import db
from models import Result
from utils import get_ranking

tables = Blueprint("tables", __name__)


@tables.route("/tables", methods=["GET"])
def get_tables():
    default_groups = [f"Group{x}" for x in "ABCDEFGH"]
    groups = request.args.get("tables", default=default_groups, type=str)
    tables = get_ranking(groups)
    return jsonify(tables), 200
