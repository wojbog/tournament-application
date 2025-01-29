import datetime
import sys
from flask import Blueprint, flash, jsonify, Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Tournament, Discipline, Result, Player
from . import db
import time
from flask_login import login_user, login_required, logout_user, current_user


main = Blueprint("main", __name__)


@main.route("/")
def index():
    current_date = datetime.datetime.now()
    tournaments = Tournament.query.filter(
        Tournament.date >= current_date).all()

    tournament_tab = []
    for tournament in tournaments:
        discipline = Discipline.query.filter_by(
            id=tournament.discipline_id).first().name
        results = Result.query.filter_by(tournament_id=tournament.id).all()
        status = ""
        if len(results) < tournament.max_participants:
            status = "Open"
        else:
            status = "Full"
        tour = Tournament(tournament.id, tournament.name, tournament.date, tournament.location,
                          discipline, status)
        tour.date = tournament.date
        tournament_tab.append(tour)

    return render_template('main.html', tournaments=tournament_tab)


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
        max_participants = request.form.get('max_participants')
        discipline = request.form.get('discipline')
        location = request.form.get('location')

        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.datetime.strptime(time, '%H:%M').time()

        discipline_obj = Discipline.query.filter_by(name=discipline).first()

        date_time = datetime.datetime.combine(date, time)

        new_tournament = Tournament(None, None, date_time, None, None, None)
        new_tournament.max_participants = int(max_participants)
        new_tournament.owner_id = current_user.id
        new_tournament.discipline_id = discipline_obj.id
        new_tournament.date = date_time
        new_tournament.location = location
        new_tournament.name = name
        new_tournament.owner_id = current_user.id

        db.session.add(new_tournament)
        db.session.commit()
        flash('Tournament created successfully!', 'success')
        return redirect(url_for('tournament.dashboard'))

    return render_template('create_tournament.html')


@tournament_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    current_date = datetime.datetime.now()
    tournaments = Tournament.query.filter(
        Tournament.date > current_date).all()

    tournament_tab = []
    for tournament in tournaments:
        discipline = Discipline.query.filter_by(
            id=tournament.discipline_id).first().name
        results = Result.query.filter_by(tournament_id=tournament.id).all()
        status = ""
        if len(results) < tournament.max_participants:
            status = "Open"
        else:
            status = "Full"
        tour = Tournament(tournament.id, tournament.name, tournament.date, tournament.location,
                          discipline, status)
        tournament_tab.append(tour)
    return render_template('dashboard.html', tournaments=tournament_tab)


@tournament_bp.route('/apply/<int:id>', methods=['GET', 'POST'])
def apply(id):

    with db.session.begin():
        db.session.connection(
            execution_options={'isolation_level': 'SERIALIZABLE'})
        tournament = db.session.query(Tournament).filter_by(id=id).first()

        if not tournament:
            flash("Tournament not found.", "error")
            return redirect(url_for("tournament.dashboard"))

        results = db.session.query(Result).filter_by(tournament_id=id).all()

        if db.session.query(Result).filter_by(tournament_id=id, user_id=current_user.id).first():
            flash("You have already applied to this tournament.", "error")
            return redirect(url_for("tournament.dashboard"))

        if tournament.max_participants <= len(results):
            flash("Tournament is full.", "error")
            return redirect(url_for("tournament.dashboard"))

        new_result = Result(
            tournament_id=id, user_id=current_user.id, result=0)

        db.session.add(new_result)
        db.session.commit()

    flash("Successfully applied to the tournament!", "success")
    return redirect(url_for("tournament.dashboard"))


@tournament_bp.route('/participation')
@login_required
def participation():

    results = db.session.query(Tournament, Result).filter(
        Tournament.id == Result.tournament_id, Result.user_id == current_user.id).all()
    tournaments = []
    for tournament, result in results:
        discipline = Discipline.query.filter_by(
            id=tournament.discipline_id).first().name
        tournaments.append(
            Tournament(tournament.id, tournament.name, tournament.date, tournament.location, discipline, ""))

    return render_template('participation.html', tournaments=tournaments)


@tournament_bp.route('/leaderboard/<int:tournament_id>')
@login_required
def leaderboard(tournament_id):
    tournament = db.session.query(
        Tournament).filter_by(id=tournament_id).first()

    if not tournament:
        flash("Tournament not found!", "error")
        return redirect(url_for('dashboard'))

    results = db.session.query(Result).filter_by(
        tournament_id=tournament_id).all()

    users = db.session.query(User).join(Result).filter(
        Result.tournament_id == tournament_id).all()

    leaderboard_data = []
    for user in users:
        for result in results:
            if user.id == result.user_id:
                leaderboard_data.append(
                    Player(user.id, user.name, 0, result.result))

    leaderboard_data.sort(key=lambda x: x.score, reverse=True)

    for i, player in enumerate(leaderboard_data):
        player.rank = i + 1

    return render_template('leaderboard.html', tournament=tournament, leaderboard=leaderboard_data)


@tournament_bp.route('/my_tournaments')
@login_required
def my_tournaments():

    tournaments = db.session.query(Tournament).filter_by(
        owner_id=current_user.id).all()

    tournaments_tab = []
    for tournament in tournaments:
        discipline = Discipline.query.filter_by(
            id=tournament.discipline_id).first().name
        tournaments_tab.append(
            Tournament(tournament.id, tournament.name, tournament.date, tournament.location, discipline, ""))

    return render_template('my_tournaments.html', tournaments=tournaments_tab)


@tournament_bp.route('/play/<int:id>', methods=['GET', 'POST'])
@login_required
def play(id):
    tournament = db.session.query(Tournament).filter_by(id=id).first()

    if not tournament:
        flash("Tournament not found!", "error")
        return redirect(url_for('tournament.dashboard'))

    if tournament.owner_id != current_user.id:
        flash("You are not the owner of this tournament!", "error")
        return redirect(url_for('tournament.dashboard'))

    results = db.session.query(Result).filter_by(
        tournament_id=id).all()
    import random
    for result in results:
        result.result = random.randint(0, 100)
        db.session.commit()

    return render_template('play.html', tournament=tournament)
