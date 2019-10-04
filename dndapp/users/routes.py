from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from dndapp import db, bcrypt
from dndapp.models import User, Character
from dndapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from dndapp.users.utils import send_reset_email
from dndapp.static.py_scripts import save_profile_picture

users = Blueprint('users', '__init__')

@users.context_processor
def inject_characters():
	# allows all templates to access the character_list variable
    return dict(character_list = Character.query.order_by(Character.date_created.desc()))


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('characters.create'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # user.password the user's password in the db
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next') # args is a dictionary
            # return redirect(next_page) if next_page else redirect(url_for('create'))
            return redirect(url_for('main.home'))
        else:
            flash(u'Login Unsuccessful. Please check email and password', 'text-danger')
    else:
        print(form.errors)
    return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('characters.create'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # encrypt password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create user with information provided by user
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # add user to database
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_profile_picture(form.picture.data)
			# current_user is imported from flask_login
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated.', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_characters(username):
    # page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    characters = Character.query.filter_by(creator=user)\
        .order_by(Character.date_posted.desc())\
        .paginate(page=page, per_page=5) # sqlalchemy
    return render_template('user_character.html', characters=characters, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # enter email to request password reset
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # reset the password with the token
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # encrypt password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated. You may now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
