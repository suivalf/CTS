import requests
from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, CoinForm
from app.models import User, Coin, load_user
from werkzeug.urls import url_parse
from app import db, app
from app.TTScripts import get_all, check_price, get_price_from_symbol, get_stringid_from_symbol
from app.MyThread import myThread


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    option_list = get_all()
    if request.method == 'GET':
        if request.args.get('option') is not None:
            c = request.args.get('option').split("-")
            coinSymbol = c[0]
            coinId = get_stringid_from_symbol(coinSymbol)
            coinName = c[1]
            coinPrice = round(float(get_price_from_symbol(coinSymbol)), 5)
            coin = Coin(coinid=coinId, symbol=coinSymbol, name=coinName, price=coinPrice)
            Coin.query.filter_by(name='None').delete()
            db.session.commit()
            found = 0
            for c in Coin.query.filter(Coin.user_id == current_user.id).all():
                if c.symbol == coinSymbol:
                    found = 1
            if found == 0:
                if coinName != 'None':
                    current_user.coins.append(coin)
                    db.session.commit()
                    flash('Your coin is now added!')
            elif found == 1:
                flash('You have this coin already!')
    owns = current_user.followed_coins()

    return render_template('index.html', coins=owns, option_list=option_list)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/playPrice/<string:symbol>", methods=['GET'])
def playPrice(symbol):
    thread = myThread(current_user.username + symbol, current_user.id, symbol)
    thread.start()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    for c in current_user.coins:
        if c.id == id:
            try:
                current_user.coins.remove(c)
                db.session.commit()
                flash('Coin removed!')
            except:
                flash('Something went wrong.')
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