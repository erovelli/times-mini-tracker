from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Group
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
import string

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ login page """

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user:  # log in user
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/group-landing', methods=['GET', 'POST'])
@login_required
def group():
    """ group landing page """

    if current_user.group_id:  # reroute user if in group
        print('hi testtyy')
        return redirect(url_for('views.group'))

    if request.method == 'POST':
        if request.form['group_key']:  # join group
            key = request.form.get('group_key')
            group = Group.query.filter_by(key=key).first()
            if group:
                group.users.append(current_user)
                db.session.commit()
                flash('Group joined!', category='success')

                return redirect(url_for('views.group'))
            else:
                flash('Group key incorrect', category='error')

        elif request.form['create'] == 'create':  # create group
            key = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=5))
            new_group = Group(key=key)
            db.session.add(new_group)
            new_group.users.append(current_user)
            db.session.commit()
            flash('Group created!', category='success')

            return redirect(url_for('views.group'))

    return render_template("group_landing.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """ logout user """

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """ sign up page """

    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already in use.', category='error')
        elif len(username) < 3:
            flash('Username must be atleast 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(username=username, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
