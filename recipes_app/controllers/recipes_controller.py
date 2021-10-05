from flask import Flask, render_template, redirect, session, request
from recipes_app import app
from recipes_app.models.recipes import Recipe
from recipes_app.models import users

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/recipes/new', methods=['GET','POST'])
def newrecipe():
    if not session:
        return redirect ('/')
    userid = session['userid']
    return render_template("newrecipe.html", user_id = userid)

@app.route('/recipe/save', methods=['POST'])
def saverecipe():
    print (request.form)
    if not Recipe.recipe_validation(request.form):
        return redirect ('/recipes/new')
    newrecipe = Recipe.saverecipe(request.form)
    return redirect ('/dashboard')

@app.route('/recipes/<int:id>')
def recipe_detail(id):
    if not session:
        return redirect ('/')
    recipe = Recipe.getsinglerecipe(id)
    data = session['userid']
    user = users.User.getuser(data)
    return render_template ("recipe.html", recipe = recipe, user = user)

@app.route('/recipes/edit/<int:id>')
def recipe_edit(id):
    if not session:
        return redirect ('/')
    data = session['userid']
    user = users.User.getuser(data)
    recipe = Recipe.getsinglerecipe(id)
    if session['userid'] != recipe['user_id']:
        return redirect ('/dashboard')
    return render_template ("editrecipe.html", recipe = recipe, user = user)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def updated_recipe(id):
    print (request.form)
    if not Recipe.recipe_validation(request.form):
        redirecturl = f"/recipes/edit/{id}"
        return redirect (redirecturl)
    updatedrecipe = Recipe.updaterecipe(request.form)
    return redirect ('/dashboard')

@app.route('/recipes/remove/<int:id>')
def remove_recipe(id):
    Recipe.remove(id)
    return redirect ('/dashboard')
