from flask import Blueprint, jsonify
from .models import User
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    # say hello world
    return jsonify({"message": "Hello, World!"})
