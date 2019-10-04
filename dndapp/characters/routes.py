from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from dndapp import db
from dndapp.models import Character
from dndapp.characters.forms import CreateForm, UpdateCharacterForm
from dndapp.static.py_scripts import score_modifier, save_character_picture

characters = Blueprint('characters', '__init__')

@characters.context_processor
def inject_characters():
	# allows all templates to access the character_list variable
    return dict(character_list = Character.query.order_by(Character.date_created.desc()))

@characters.route("/create", methods=['GET', 'POST'])
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
        return redirect(url_for('main.home'))
    else:
        print(form.errors)
    return render_template('create.html', title='New Character', form=form, legend='New Character')

@characters.route("/character/<int:character_id>", methods=['GET', 'POST'])
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
        return redirect(url_for('characters.character', character_id=character.id))
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
