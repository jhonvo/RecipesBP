from flask import Flask, render_template, redirect, session, request
from recipes_app import app
from recipes_app.models.users import User
from recipes_app.models import recipes

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    if not session:
        return render_template('index.html')
    return redirect ('/dashboard')

@app.route('/register', methods=['POST'])
def register():
    if not User.register_validation(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : pw_hash,
        'email' : request.form['email'],
        }
    newUser = User.register(data)
    session['userid'] = newUser
    return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    if not User.login_validation(request.form):
        return redirect ('/')
    return redirect ('/dashboard')

@app.route('/dashboard')
def user():
    if not session:
        return redirect ('/')
    data = session['userid']
    user = User.getuser(data)
    recipelist = recipes.Recipe.getallrecipes()
    return render_template('dashboard.html', recipes = recipelist, user = user)

@app.route('/logout', methods=['GET'])
def restart():
    session.clear()
    return redirect('/')