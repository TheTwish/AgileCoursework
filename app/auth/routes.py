from flask import Flask, request, Blueprint, render_template, flash, \
                redirect, url_for, request, session
from app.auth.forms import LoginForm, RegistrationForm, \
                            ResetPasswordForm,ResetPasswordRequestForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db, mail
from werkzeug.urls import url_parse
from app.auth.email import send_password_reset_email, send_verify_email
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

auth = Blueprint('auth', __name__)

"""s = URLSafeTimedSerializer('Thisisasecret!')
app = Flask(__name__)
app.config.from_pyfile('config.py')"""

"""@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        validated = User.query.filter_by(username=form.username.data, validated=True).first()
        
        if validated:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            flash("You are now signed in!", "success")
            return redirect(next_page)
        flash('User is not validated, please check your email', 'danger')
    return render_template('auth/login.html', title='Login', form=form)"""

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        if not user.validated:
            flash('Email not validated!!!', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash("You are now signed in!", "success")
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            first_name=form.first_name.data.lower(),
            last_name=form.last_name.data.lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        """email = request.form['email']
        token = s.dumps(form.username.data,salt='email-confirm')
        msg = Message('Confirm Email', sender='fakenameminecraft@gmail.com', recipients=[form.email.data])
        link = url_for('auth.confirm_email',token=token,_external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)"""

        send_verify_email(user)

        flash('Please check your email to validate your registration', 'success')
        return(redirect(url_for('main.index')))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash("You've signed out!", "success")
    return redirect(url_for('main.index'))

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occured, please try again', 'danger')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    user = User.verify_token_user(token)
    if not user:
        return redirect(url_for('main.index'))
    """try:
        email = s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return '<h1>Your link has expired!<h1>'"""

    user.set_validated(True)
    db.session.commit()
    flash('You are now authenticated, congratulations!', 'success')
    return redirect(url_for('auth.login'))