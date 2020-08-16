from flask import Flask

from cl_blueprints import results, tables
from extensions import db


def register_extensions(app):
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cl.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(results)
    app.register_blueprint(tables)

    register_extensions(app)

    return app


app = create_app()
