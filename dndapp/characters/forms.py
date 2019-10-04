from dndapp.models import User
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class CreateForm(FlaskForm):
    name = StringField(u'Name', validators=[DataRequired(), Length(max=30)])
    race = SelectField(u'Race', choices=[('Dwarf', 'dwarf'), ('Elf', 'elf'), ('Halfling', 'halfling'),
                                        ('Human', 'human'), ('Dragonborn', 'dragonborn'), ('Gnome', 'gnome'),
                                        ('Half-Orc', 'half-orc'), ('Half-Elf', 'half-elf'),
                                        ('Tiefling', 'tiefling')], validators=[DataRequired()])
    char_class = SelectField(u'Class', choices=[('Barbarian', 'Barbarian'), ('Bard', 'Bard'),
                                        ('Cleric', 'Cleric'), ('Druid', 'Druid'), ('Fighter', 'Fighter'),
                                        ('Monk', 'Monk'), ('Paladin', 'Paladin'), ('Ranger', 'Ranger'),
                                        ('Rogue', 'Rogue'), ('Sorcerer', 'Sorcerer'), ('Warlock', 'Warlock'),
                                        ('Wizard', 'Wizard')], validators=[DataRequired()])
    armour_class = IntegerField(u'AC', validators=[DataRequired()])
    hit_points = IntegerField(u'HP', validators=[DataRequired()])
    gender = StringField(u'Gender', validators=[Length(max=10)])
    age = IntegerField(u'Age', validators=[DataRequired()])
    strength = IntegerField(u'Str', validators=[DataRequired()])
    constitution = IntegerField(u'Con', validators=[DataRequired()])
    dexterity = IntegerField(u'Dex', validators=[DataRequired()])
    wisdom = IntegerField(u'Wis', validators=[DataRequired()])
    intelligence = IntegerField(u'Int', validators=[DataRequired()])
    charisma = IntegerField(u'Cha', validators=[DataRequired()])
    short_bio = TextAreaField(u'Short Bio', validators=[Length(max=250)])
    long_bio = TextAreaField(u'Character Background', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    notes = TextAreaField(u'Field Notes')
    submit = SubmitField('Create')

class UpdateCharacterForm(FlaskForm):
    save = SubmitField('Save')
    long_bio = TextAreaField('Character Background')
    short_bio = TextAreaField('Quick Info')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    notes = TextAreaField('Field Notes')
    current_hp = IntegerField('Hit Points')
    hp_change = IntegerField(validators=[NumberRange(min=0, max=999, message="Enter value between 0 and 999")])
    heal_submit = SubmitField(label="Heal")
    dmg_submit = SubmitField(label="Damage")
