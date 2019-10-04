from flask import render_template, request, Blueprint
from dndapp.models import Character

main = Blueprint('main', '__init__')

@main.context_processor
def inject_characters():
	# allows all templates to access the character_list variable
    return dict(character_list = Character.query.order_by(Character.date_created.desc()))

@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html')

@main.route("/about")
def about():
	return render_template('about.html', title='About')
