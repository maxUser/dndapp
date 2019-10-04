import secrets
import os
from PIL import Image # for resizing images
from flask import current_app

def test_function():
    print('Testing, 1, 2, 3!')

# save the user's uploaded image to the file system (in profile_pics)
def save_profile_picture(form_picture):
    # pictures will be named a random hex
    random_hex = secrets.token_hex(8)
    # form_picture is the data from the field the user submits
    _, f_ext = os.path.splitext(form_picture.filename) # the lone underscore represents an unused variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # resize image
    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # ########
    # TO DO
    # Delete old profile pics when user changes to a new one
    # ########

    i.save(picture_path)

    return picture_fn

def save_character_picture(form_picture):
    # pictures will be named a random hex
    random_hex = secrets.token_hex(8)
    # form_picture is the data from the field the user submits
    _, f_ext = os.path.splitext(form_picture.filename) # the lone underscore represents an unused variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/character_pics', picture_fn)
    # resize image
    output_size = (220, 220)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # ########
    # TO DO
    # Delete old profile pics when user changes to a new one
    # ########

    i.save(picture_path)
    return picture_fn

def calculate_modifier(score):
	if score == 1:
		return -5
	elif score == 2 or score == 3:
		return -4
	elif score == 4 or score == 5:
		return -3
	elif score == 6 or score == 7:
		return -2
	elif score == 8 or score == 9:
		return -1
	elif score == 10 or score == 11:
		return 0
	elif score == 12 or score == 13:
		return 1
	elif score == 14 or score == 15:
		return 2
	elif score == 16 or score == 17:
		return 3
	elif score == 18 or score == 19:
		return 4
	elif score == 20 or score == 21:
		return 5
	elif score == 22 or score == 23:
		return 6
	elif score == 24 or score == 25:
		return 7
	elif score == 26 or score == 27:
		return 8
	elif score == 28 or score == 29:
		return 9
	elif score == 30:
		return 10

def score_modifier(character):
	str_mod = calculate_modifier(character.strength)
	con_mod = calculate_modifier(character.constitution)
	dex_mod = calculate_modifier(character.dexterity)
	wis_mod = calculate_modifier(character.wisdom)
	int_mod = calculate_modifier(character.intelligence)
	cha_mod = calculate_modifier(character.charisma)
	mod_dict = {"strength":str_mod, "constitution":con_mod, "dexterity": dex_mod,
				"wisdom": wis_mod, "intelligence": int_mod, "charisma": cha_mod}
	return mod_dict
