from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from ai_predictor import predict_stock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    profile_pic = db.Column(db.String(150), nullable=True)
    bio = db.Column(db.Text, nullable=True)

# Stock model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='sha256')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(id=session['user_id']).first()
    stocks = Stock.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, stocks=stocks)

@app.route('/ai-predictor')
def ai_predictor():
    predictions = predict_stock(['AAPL', 'GOOGL', 'AMZN'])
    return render_template('ai_predicter.html', predictions=predictions)

@app.route('/fake-money', methods=['GET', 'POST'])
def fake_money():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        purchase_price = float(request.form['purchase_price'])

        new_stock = Stock(user_id=session['user_id'], symbol=symbol, quantity=quantity, purchase_price=purchase_price)
        db.session.add(new_stock)
        db.session.commit()

        return redirect(url_for('profile'))

    return render_template('fake_money.html')

@app.route('/graph-and-statistics')
def graph_and_statistics():
    # Here you would pass in actual stock data and AI predictions
    return render_template('graph_and_statistics.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
