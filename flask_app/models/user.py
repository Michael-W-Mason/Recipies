#  This is a template for how to do a basic query of the databse. This exampe shows how to pull and create data.

# Allows us to connect to our database and query it
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Create A Class of our DB table
class User:
    db = 'recipe_schema'
    # We pass in our data as a dict
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
    
    @staticmethod
    def validate_user_registration(data):
        is_valid = True
        if not re.fullmatch(EMAIL_REGEX, data['email']):
            flash('Invalid Email', 'reg')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_login(data):
        user = User.get_user_by_email(data)
        if user == None:
            flash('Incorrect email / password', 'login')
            return False
        if not bcrypt.check_password_hash(user.password, data['password']):
            flash('Wrong Password', 'login')
            return False           
        return True
    
    @classmethod
    def insert_row(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == ():
            return None
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id=%(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == ():
            return None
        return cls(result[0])