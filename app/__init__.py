import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
pymysql.install_as_MySQLdb()


def create_app():

    app = Flask(__name__)

    username = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database_name = os.getenv("DATABASE_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + \
        username+":"+password+"@"+host+":"+port+"/"+database_name

    db.init_app(app)

    # create tables
    with app.app_context():
        db.create_all()

    from .routers import main
    app.register_blueprint(main)

    return app
