from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, CoinForm
from app.models import User, Coin, load_user
from werkzeug.urls import url_parse
from app import db, app
from app.TTScripts import get_all

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    option_list = get_all()
    coinName = request.args.get('option')
    coin = Coin(name=coinName)
    Coin.query.filter_by(name='None').delete()
    db.session.commit()
    found = 0
    print(coinName)
    for c in Coin.query.filter(Coin.user_id == current_user.id).all():
        if c.name == coinName:
            found = 1
    if found == 0:
        if coinName != 'None':
            current_user.coins.append(coin)
            db.session.commit()
            flash('Your coin is now added!')
    elif found == 1 and coinName != 'None':
        flash('You own this coin already')
    owns = current_user.followed_coins()

    return render_template('index.html', coins=owns, option_list=option_list, coinName=coinName)


@app.route('/delete/<int:id>')
def delete(id):
    for c in current_user.coins:
        if c.id == id:
            try:
                current_user.coins.remove(c)
                db.session.commit()
            except:
                flash('You own this coin already')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or passowrd!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)