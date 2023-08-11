from random import choice
import string
from flask import render_template, url_for, flash, redirect, request
from nittly import app, db, bcrypt
from nittly.forms import RegistrationForm, LoginForm, UrlForm
from nittly.models import User, Url
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def generate_short_id(length):
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(length))

@app.route("/shorten", methods=['GET', 'POST'])
@login_required
def shorten():
    form=UrlForm()
    if form.validate_on_submit():
        if form.original_url.data:
            short_id=form.short_id.data
            if not form.short_id.data:
                random_id=generate_short_id(8)
                while(Url.query.filter_by(short_id=random_id).first()):
                    random_id=generate_short_id(8)
                short_id=random_id    
            new_link = Url(original_url=form.original_url.data, short_id=short_id, user=current_user)
            db.session.add(new_link)
            db.session.commit()

            shortened_url=request.host_url + short_id

            return render_template('shorten.html',form=form,shortened_url=shortened_url,short_id=short_id)
    
    return render_template('shorten.html',form=form)

@app.route("/<short_id>", methods=['GET', 'POST'])
@login_required
def redirect_url(short_id):
    link=Url.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL','danger')
        return redirect(url_for('home'))
    

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
        user=User.query.filter_by(username=current_user.username).first()
        urls=user.urls       
        host_url=request.host_url
        return render_template('account.html',urls=urls,user=user,host_url=host_url)