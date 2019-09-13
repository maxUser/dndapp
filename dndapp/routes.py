import os
import secrets
from PIL import Image # for resizing images
from flask import render_template, url_for, flash, redirect, request, abort
from dndapp.static.py_scripts import score_modifier, save_character_picture, save_profile_picture
from dndapp import app, db, bcrypt
from dndapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateForm, UpdateCharacterForm
from dndapp.models import User, Character
from flask_login import login_user, current_user, logout_user, login_required
from flask import send_from_directory
from sqlalchemy import update

@app.route('/favicon.ico')
def favicon():
    # deals with "GET /favicon.ico HTTP/1.1" 404
    # source: https://stackoverflow.com/questions/30957203/trying-to-locate-404-error-running-python-flask-with-bootstrap
    # NOT WORKING
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.context_processor
def inject_characters():
	# allows all templates to access the character_list variable
    return dict(character_list = Character.query.order_by(Character.date_created.desc()))

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('create'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # user.password the user's password in the db
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # next_page = request.args.get('next') # args is a dictionary
            # return redirect(next_page) if next_page else redirect(url_for('create'))
            return redirect(url_for('home'))
        else:
            flash(u'Login Unsuccessful. Please check email and password', 'text-danger')
    else:
        print(form.errors)
    return render_template('login.html', title='login', form=form)

@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('create'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        print(form.gender.data)
        if not form.gender.data:
            form.gender.data = 'N/A'
        print(form.gender.data)
        character = Character(creator=current_user, name=form.name.data, race=form.race.data,
							char_class=form.char_class.data, gender=form.gender.data,
							age=form.age.data, strength=form.strength.data,
							constitution=form.constitution.data, dexterity=form.dexterity.data,
							wisdom=form.wisdom.data, intelligence=form.intelligence.data,
							charisma=form.charisma.data, long_bio=form.long_bio.data,
							short_bio=form.short_bio.data, notes=form.notes.data,
                            armour_class=form.armour_class.data, hit_points=form.hit_points.data)
        db.session.add(character)
        db.session.commit()
        flash(f'{form.name.data} has been created!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('create.html', title='New Character', form=form, legend='New Character')

@app.route("/character/<int:character_id>", methods=['GET', 'POST'])
@login_required
def character(character_id):
    character = Character.query.get_or_404(character_id)
    if character.creator != current_user:
        abort(403)

    form = UpdateCharacterForm()

    modifiers = score_modifier(character)
    if character.current_hp == None:
        character.current_hp = character.hit_points

    if form.hp_change.data is None:
        form.hp_change.data = 0

    # print('form.picture.data: {}'.format(form.picture.data))

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_character_picture(form.picture.data)
            character.image_file = picture_file

        if form.heal_submit.data:
            if character.current_hp + form.hp_change.data > character.hit_points:
                character.current_hp = character.hit_points
            else:
                character.current_hp = character.current_hp + form.hp_change.data

        elif form.dmg_submit.data:
            character.current_hp = character.current_hp - form.hp_change.data

        character.notes = form.notes.data
        character.long_bio = form.long_bio.data

        db.session.commit()

        flash('Character sheet updated!', 'success')
        return redirect(url_for('character', character_id=character.id))
    elif request.method == 'GET':
        form.notes.data = character.notes
        form.long_bio.data = character.long_bio
        form.short_bio.data = character.short_bio
    else:
        print('Errors', form.errors)

    image_file = url_for('static', filename='character_pics/' + character.image_file)
    return render_template('character.html', title=character.name,
    						character=character, image_file=image_file,
    						form=form, modifiers=modifiers)


@app.route("/account", methods=['GET', 'POST'])
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
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/example")
def example():
	image_file = url_for('static', filename='profile_pics/muradin.jpg')
	return render_template('example.html', title='Example Character', image_file=image_file)




@app.route("/user/<string:username>")
def user_characters(username):
    # page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    characters = Character.query.filter_by(creator=user)\
        .order_by(Character.date_posted.desc())\
        .paginate(page=page, per_page=5) # sqlalchemy
    return render_template('user_character.html', characters=characters, user=user)
