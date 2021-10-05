from recipes_app.config.mysqlconnection import connectToMySQL
from recipes_app import app
from recipes_app.models import users
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.lessthan30 = data['lessthan30']
        self.user_id = data['user_id']
    
    @classmethod
    def getallrecipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('precipes_bp').query_db(query)
        recipelist = []
        for line in results:
            recipelist.append(Recipe(line))
        return recipelist

    @staticmethod
    def recipe_validation(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Please provide a valid Name")
            is_valid=False
        if len(data['description']) < 3:
            flash("Please provide a valid Description.")
            is_valid=False
        if len(data['instructions']) < 3:
            flash("Please provide valid Instructions")
            is_valid=False
        if len(data['description']) > 300:
            flash("Description can not be more than 300 characters.")
            is_valid=False
        if len(data['instructions']) > 2000:
            flash("Instructions can not be more than 2000 characters.")
            is_valid=False
        if data['date'] == "":
            flash("Please select a date.")
            is_valid=False
        if data['lessthan30'] == 'None':
            flash("Please confirm if the recipe is under 30 minutes or not.")
            is_valid=False
        return is_valid

    @classmethod
    def saverecipe(cls,data):
        query = "INSERT INTO recipes (date,description,instructions,lessthan30,name,user_id) VALUES (%(date)s,%(description)s,%(instructions)s,%(lessthan30)s,%(name)s,%(user_id)s);"
        results = connectToMySQL('precipes_bp').query_db(query,data)
        return results

    @classmethod
    def updaterecipe(cls,data):
        query = "UPDATE recipes SET  date = %(date)s, description = %(description)s, instructions = %(instructions)s, lessthan30 = %(lessthan30)s, name = %(name)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('precipes_bp').query_db(query,data)
        return results

    @classmethod
    def getsinglerecipe(cls,id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        data = {
            'id' : id
        }
        results = connectToMySQL('precipes_bp').query_db(query,data)
        return results[0]

    @classmethod
    def remove (cls,id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {
            'id' : id
        }
        results = connectToMySQL('precipes_bp').query_db(query,data)
        return results