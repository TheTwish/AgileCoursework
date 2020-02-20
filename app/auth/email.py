from flask import render_template, current_app
from app.email import send_email

APP_NAME = "What's on"


def send_password_reset_email(user):
    token = user.get_token()
    send_email(
        f'{APP_NAME} : Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/reset_password.txt',
            user=user, token=token),
        html_body=render_template(
            'email/reset_password.html',
            user=user, token=token)
    ) 

def send_verify_email(user):
    token = user.get_token()
    send_email(
        f'{APP_NAME} : Verify Your email',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/Verify.txt',
            user=user, token=token),
        html_body=render_template(
            'email/Verify.html',
            user=user, token=token)
    )
