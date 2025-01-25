import datetime
from flask import Blueprint, flash, jsonify, Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Tournament, Discipline, Result
from . import db
import time
from flask_login import login_user, login_required, logout_user, current_user


main = Blueprint("main", __name__)


@main.route("/")
def index():
    # get current data
    current_date = time.time()

    print("elo")
    print(current_date)
    # get data from database tournament table
    tournaments = Tournament.query.all()

    return render_template('main.html', tournaments=tournaments)


auth_bp = Blueprint('auth', __name__, template_folder='../templates')
tournament_bp = Blueprint('tournament', __name__,
                          template_folder='../templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')

        password_hash = generate_password_hash(password)

        new_user = User(name=name, surname=surname,
                        email=email, password=password_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.success'))
        except Exception as e:
            return f"An error occurred: {e}", 500

    return render_template('register.html')


@tournament_bp.route('/logout', methods=['GET'])
def log_out():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/success')
def success():
    return render_template('success_register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return redirect(url_for('auth.login'))

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('tournament.dashboard'))

        return redirect(url_for('auth.login'))

    return render_template('login.html')


@tournament_bp.route('/tournament', methods=['GET', 'POST'])
@login_required
def create_tournament():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        time = request.form.get('time')
        limit_of_participants = request.form.get('limit_of_participants')
        discipline = request.form.get('discipline')
        location = request.form.get('location')

        # convert date and time to datetime
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time, '%H:%M').time()

        discipline_obj = Discipline.query.filter_by(name=discipline).first()
        print(discipline_obj)
        # wait
        date_time = datetime.datetime.combine(date, time)

        new_tournament = Tournament(
            name=name,
            date=date_time,
            max_participants=int(limit_of_participants),
            discipline_id=discipline_obj.id,
            location=location,
            owner_id=current_user.id
        )
        db.session.add(new_tournament)
        db.session.commit()
        flash('Tournament created successfully!', 'success')
        return redirect(url_for('tournament.dashboard'))

    return render_template('create_tournament.html')


@tournament_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    tournaments = Tournament.query.all()

    return render_template('dashboard.html', tournaments=tournaments)
