import datetime
import re
import uuid

from sqlalchemy import text

from extensions import db

sql_command = """select distinct away_team as team_, stage, gf1 + ifnull(gf2, 0) as gf, ga1 + ifnull(ga2, 0)  as ga, w1 + ifnull(w2, 0) as w, d1 + ifnull(d2, 0) as d, l1 + ifnull(l2, 0) as l, gf1 + ifnull(gf2, 0) - ga1 - ifnull(ga2, 0) as gd,  (w1 + ifnull(w2, 0)) * 3 + d1 + ifnull(d2, 0) as points
from (SELECT          *
FROM            (
                         SELECT   away_team,
                                  stage,
                                  Sum(away_score)                   AS gf1,
                                  Sum(home_score)                   AS ga1,
                                  Sum(away_score - home_score > 0)  AS w1,
                                  sum(home_score - away_score IS 0) AS d1,
                                  sum(away_score - home_score < 0)  AS l1
                         FROM     result
                         GROUP BY away_team) AS a
LEFT OUTER JOIN
                (
                         SELECT   home_team,
                                  stage,
                                  sum(home_score)                   AS gf2,
                                  sum(away_score)                   AS ga2,
                                  sum(home_score - away_score > 0)  AS w2,
                                  sum(home_score - away_score IS 0) AS d2,
                                  sum(home_score - away_score < 0)  AS l2
                         FROM     result
                         GROUP BY home_team) AS b
ON              a.away_team = b.home_team
UNION ALL
SELECT          *
FROM            (
                         SELECT   home_team,
                                  stage,
                                  sum(home_score)                   AS gf2,
                                  sum(away_score)                   AS ga2,
                                  sum(home_score - away_score > 0)  AS w2,
                                  sum(home_score - away_score IS 0) AS d2,
                                  sum(home_score - away_score < 0)  AS l2
                         FROM     result
                         GROUP BY home_team) AS a
LEFT OUTER JOIN
                (
                         SELECT   away_team,
                                  stage,
                                  sum(away_score)                   AS gf1,
                                  sum(home_score)                   AS ga1,
                                  sum(away_score - home_score > 0)  AS w1,
                                  sum(home_score - away_score IS 0) AS d1,
                                  sum(away_score - home_score < 0)  AS l1
                         FROM     result
                         GROUP BY away_team) AS b
ON              a.home_team = b.away_team)
where stage is "{}"
order by points DESC, gd DESC, gf DESC; """  # noqa E501


def get_match_uuid(match_dict):
    name = f"{match_dict['home_team']}{match_dict['away_team']}{match_dict['match_time']}"  # noqa E501
    return str(uuid.uuid5(uuid.NAMESPACE_X500, name))


def validate_input(data):
    message = ""
    if not data.get("home_team"):
        message += "No home_team provided.\n"
    if not data.get("away_team"):
        message += "No away_team provided.\n"
    if (
        not data.get("score")
        or re.fullmatch(r"[0-9]{1,3}:[0-9]{1,3}", data.get("score")) is None
    ):
        message += "No score provided or score in bad format.\n"
    if (
        not data.get("stage")
        or re.fullmatch(r"Group[A-H]{1}", data.get("stage")) is None
    ):
        message += "No stage provided or stage in bad format.\n"
    if not data.get("match_time"):
        message += "No match_time provided.\n"
    try:
        _ = datetime.datetime.strptime(data.get("match_time"), "%Y-%m-%dT%H:%M")  # noqa E501
    except ValueError:
        message += "Bad format of match_time.\n"
    return message.strip()


def get_ranking(groups):
    return_list = []
    for group in groups:
        group_dict = {group: []}
        ranking = get_table(group)
        for rank, team in enumerate(ranking):
            team_dict = {
                "rank": rank + 1,
                "team": team[0],
                "goals_for": team[2],
                "goals_against": team[3],
                "wins": team[4],
                "draws": team[5],
                "defeats": team[6],
                "goal_difference": team[7],
                "points": team[8],
            }
            group_dict[group].append(team_dict)
        if ranking:
            return_list.append(group_dict)
    return return_list


def get_table(cl_group):
    sql_text = text(sql_command.format(cl_group))
    result = db.engine.execute(sql_text)
    return result.fetchall()
