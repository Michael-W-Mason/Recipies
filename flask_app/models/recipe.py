#  This is a template for how to do a basic query of the databse. This exampe shows how to pull and create data.

# Allows us to connect to our database and query it
from flask_app.config.mysqlconnection import connectToMySQL

# Create A Class of our DB table
class Recipe :
    db = 'recipe_schema'
    # We pass in our data as a dict
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.thirty_minutes = data['thirty_minutes']
        self.user_id = data['user_id']

    @classmethod
    def get_all_rows(cls):
        query = 'SELECT * FROM recipes'
        results = connectToMySQL(cls.db).query_db(query)
        if results == {}:
            return None
        rows = []
        for result in results:
            rows.append(cls(result))
        return rows

    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes WHERE id=%(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == {}:
            return None
        return cls(result[0])

    @classmethod
    def remove_recipe_by_id(cls, data):
        query = 'DELETE FROM recipes WHERE id=%(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def insert_row(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, date, thirty_minutes, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(thirty_minutes)s, %(user_id)s);'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
    
    @classmethod
    def update_row(cls, data):
        query = 'UPDATE recipes SET name=%(name)s, date=%(date)s, instructions=%(instructions)s, thirty_minutes=%(thirty_minutes)s, description=%(description)s WHERE id=%(id)s'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result