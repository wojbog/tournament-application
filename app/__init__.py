import pymysql
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager


db = SQLAlchemy()

pymysql.install_as_MySQLdb()


def create_app():

    app = Flask(__name__)
    username = os.getenv("DATABASE_USER")
    password = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOST")
    port = os.getenv("DATABASE_PORT")
    database_name = os.getenv("DATABASE_NAME")
    secret_key = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + \
        username+":"+password+"@"+host+":"+port+"/"+database_name

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.config['SECRET_KEY'] = secret_key

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    try:
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print("Database connection failed:", str(e))

    with app.app_context():
        from .models import User, Discipline, Tournament
        db.create_all()
        print("Database created!")

    from .routers import main, auth_bp, tournament_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(tournament_bp, url_prefix='/app')

    return app
