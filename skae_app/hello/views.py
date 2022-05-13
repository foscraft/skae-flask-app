from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import re
from skae_app.hello.models import create_database

skaes = Blueprint('skaes', __name__)

@skaes.route('/')
@skaes.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        create_database()
        conn = sqlite3.connect('demo_database')
        c = conn.cursor()
        c.execute("SELECT * FROM users_table WHERE username = ? AND password = ?", (username, password))
        acc = c.fetchone()
        if acc:
            session['loggedin'] = True
            session['username'] = username
            message = 'You are now logged in'
            #return redirect(url_for('skae.home'))
            return render_template('index.html', message=message)
        else:
            message = 'Invalid Credentials. Please try again.'
    return render_template('login.html', message=message)

@skaes.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))


@skaes.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect('demo_database')
        c = conn.cursor()
        c.execute("SELECT * FROM users_table WHERE email = ?", (email,))
        acc = c.fetchone()
        if acc:
            message = 'Email already registered to an account.'
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            message = 'Invalid email.'
        else:
            c.execute("INSERT INTO users_table (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            message = 'You are now registered and can log in.'
    return render_template('register.html', message=message)


@skaes.route('/profile')
def profile():
    return render_template('profile.html') if session.get('loggedin') else redirect(url_for('login'))
    
