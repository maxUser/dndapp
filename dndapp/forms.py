from dndapp.models import User
from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        # disallows users from registering with an already registered username
        # username.data is coming from the form (line 7)
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        # disallows users from registering with an already registered email
        # email.data is coming from the form (line 7)
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            # username.data is coming from the form (line 7)
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists.')

    def validate_email(self, email):
        if email.data != current_user.email:
            # email.data is coming from the form (line 7)
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered.')

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
    short_bio = StringField(u'Short Bio', validators=[Length(max=150)])
    long_bio = TextAreaField(u'Background', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    notes = TextAreaField(u'Notes')
    submit = SubmitField('Create')

class UpdateCharacterForm(FlaskForm):
    save = SubmitField('Save')
    long_bio = TextAreaField('Background')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    notes = TextAreaField('Notes')
    current_hp = IntegerField()

    hp_change = IntegerField(validators=[NumberRange(min=0, max=999, message="Enter value between 0 and 999")])
    heal_submit = SubmitField(label="Heal")
    dmg_submit = SubmitField(label="Damage")
