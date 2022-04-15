#  This is a template for how to do a basic query of the databse. This exampe shows how to pull and create data.

# Allows us to connect to our database and query it
from flask_app.config.mysqlconnection import connectToMySQL

# Create A Class of our DB table
class User:
    # We pass in our data as a dict
    def __init__(self, data):
        self.id = data['id']
        self.value = data['value']

    # 
    @classmethod
    def get_all_rows(cls):
        # MySQL query
        query = "SELECT * FROM table.row;"
        # Results returns a list of dictionaries
        results = connectToMySQL("schema_name").query_db(query)

        # Takes our results and converts a list of dicts to a list of our User instances 
        all_rows = []
        for row in results:
            all_rows.append(User(row))
        # Returns a list of instances
        return all_rows

    @classmethod
    def insert_row(cls, data):
        # MySQL Query
        query = "INSERT INTO table (column_name_1, column_name_2, ...) VALUES (%(value_name_1)s, %(value_name_2)s, ...);"
        results = connectToMySQL("schema_name").query_db(query, data)
        # return prints if successful
        return results