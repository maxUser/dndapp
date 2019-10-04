import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from dndapp import mail

def send_reset_email(user):
    print('EMAIL_USER={}'.format(os.environ.get('EMAIL_USER')))
    print(os.environ.get('EMAIL_PASS'))
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, ignore this email.
'''
    mail.send(msg)
