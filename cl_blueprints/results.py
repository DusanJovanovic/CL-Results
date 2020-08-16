import datetime

from flask import Blueprint, jsonify, request

from extensions import db
from models import Result
from utils import get_match_uuid, validate_input, get_ranking

results = Blueprint("results", __name__)


@results.route('/results', methods=["POST"])
def post_results():
    data = request.get_json(force=True)
    for res in data:
        message = validate_input(res)
        if message:
            return jsonify({"error": "400", "message": message}), 400
        else:
            res = Result(
                match_uuid=get_match_uuid(res),
                stage=res["stage"],
                home_team=res["home_team"],
                away_team=res["away_team"],
                home_score=res["score"].split(":")[0],
                away_score=res["score"].split(":")[-1],
                match_time=datetime.datetime.strptime(res["match_time"], "%Y-%m-%dT%H:%M"),
            )
            db.session.add(res)
    db.session.commit()
    groups = [f"Group{x}" for x in "ABCDEFGH"]
    tables = get_ranking(groups)
    return jsonify(tables), 201


@results.route('/results', methods=["GET"])
def get_results():
    return_list = []
    since = request.args.get('since', default="", type=str)
    until = request.args.get('until', default="", type=str)
    team = request.args.get('team', default="", type=str)
    group = request.args.get('group', default="", type=str)
    res = Result.query.filter()
    if since:
        res = res.filter(Result.match_time>=since)
    if until:
        res = res.filter(Result.match_time<=until)
    if team:
        res = res.filter((Result.away_team==team) | (Result.home_team==team))
    if group:
        res = res.filter(Result.stage==group)
    for match in res.all():
        return_list.append(match.serialize())
    return jsonify(return_list), 200
