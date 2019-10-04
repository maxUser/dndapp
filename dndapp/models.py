from dndapp import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # backref: author data is remembered, but not shown in a column
    characters = db.relationship('Character', backref='creator', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    armour_class = db.Column(db.Integer, nullable=False)
    hit_points = db.Column(db.Integer, nullable=False)
    race = db.Column(db.String(), nullable=False)
    char_class = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
    # ####
    # SHORT BIO
    # i.e. height, weight, alignment, bonds, flaws, languages
    # ####
    short_bio = db.Column(db.Text, nullable=True)
    long_bio = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default-char.png')
    notes = db.Column(db.Text, nullable=True)
    current_hp = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # how our object is represented when printed
    def __repr__(self):
        return f"Character('{self.name}', '{self.race}', '{self.char_class}', '{self.gender}', '{self.age}')"
