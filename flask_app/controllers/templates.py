from flask_app import app

# Imports all the methods our app will use
from flask import render_template, redirect, request

# Sample on how we get class from our models
from flask_app.models.template import User

# Routing
@app.route("/")
def main():
    return render_template("template.html")

# Routing with Post and redirect
@app.route("/sample_post", methods = ["POST"])
def main_post():
    # Print our form to make sure its working
    print(request.form) 
    return redirect("/")