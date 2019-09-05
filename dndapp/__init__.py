from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import create_engine


app = Flask(__name__)

app.config['SECRET_KEY'] = '87511cc2acaa9d0e6430183937360cf4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'text-warning'

from dndapp import routes
