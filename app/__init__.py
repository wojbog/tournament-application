import pymysql
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
db = SQLAlchemy()

pymysql.install_as_MySQLdb()


def create_app():

    app = Flask(__name__)

    username = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database_name = os.getenv("DATABASE_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + \
        username+":"+password+"@"+host+":"+port+"/"+database_name

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)

    try:
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print("Database connection failed:", str(e))

    with app.app_context():
        from .models import User
        db.create_all()

    from .routers import main
    app.register_blueprint(main)

    return app
