from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint


DATABASE = "recipes"

class Recipe:
    
    
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.user = data['first_name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    def show_name(self):
        return self.name
    
    #! CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_cooked, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    #! READ ALL 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        recipes = []
        for recipe_dict in results:
            recipes.append(cls(recipe_dict))
        return recipes
    
    #! READ ONE
    @classmethod
    def get_recipe(cls, id):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        data = {'id': id}
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result[0])
        recipe = Recipe(result[0])
        return recipe
    
    #! UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, date_cooked=%(date_cooked)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #! DELETE
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {
            'id':id
        }
        return connectToMySQL(DATABASE).query_db(query, data)
        

    @staticmethod
    def validate_recipe(recipe:dict):
        is_valid = True
        if len(recipe['name']) < 2:
            flash('name must be at least 2 characters')
            is_valid = False
        if len(recipe['description']) < 5:
            flash('description must be at least 5 characters')
            is_valid = False
        if len(recipe['instructions']) < 5:
            flash('instructions must be at least 5 characters')
            is_valid = False
        if len(recipe['instructions']) < 10:
            flash('instructions must be at least 10 characters')
            is_valid = False
        if len(recipe['date_cooked']) == '':
            flash('Please select a date')
            is_valid = False
        if 'under_30' not in recipe:
            flash('Please select a value')
            is_valid = False



        return is_valid