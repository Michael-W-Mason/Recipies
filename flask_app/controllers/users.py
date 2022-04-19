from flask_app import app

# Imports all the methods our app will use
from flask import render_template, redirect, request, session

# Sample on how we get class from our models
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

# For our passwords
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ----------------------------------------------------------------------
# Main Login / Reg Page
# ----------------------------------------------------------------------
@app.route('/')
def main():
    return render_template('main.html')

# ----------------------------------------------------------------------
# Registration Form Route
# ----------------------------------------------------------------------
@app.route('/register', methods =["POST"])
def register():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password'],
        'confirm_password' : request.form['confirm_password']
    }
    if(User.validate_user_registration(data)):
        del data['confirm_password']
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data['password'] = pw_hash
        user_id = User.insert_row(data)
        session['user_id'] = user_id
        return redirect('/dashboard')
    return redirect('/')

# ----------------------------------------------------------------------
# Login Form Route
# ----------------------------------------------------------------------
@app.route('/login', methods=["POST"])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    if(User.validate_user_login(data)):
        user = User.get_user_by_email(data)
        session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('/')

# ----------------------------------------------------------------------
# Dashboard Page
# ----------------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    if("user_id" in session):
        data = {
            'id' : session['user_id']
        }
        user = User.get_user_by_id(data)
        recipes = Recipe.get_all_rows()
        return render_template('dashboard.html', user=user, recipes=recipes)
    return redirect('/')

# ----------------------------------------------------------------------
# Logout
# ----------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ----------------------------------------------------------------------
# New Recipe Page
# ----------------------------------------------------------------------
@app.route('/recipes/new')
def new_recipe():
    if("user_id" in session):
            return render_template('new_recipe.html')
    return redirect('/')

# ----------------------------------------------------------------------
# New Recipe Form Route
# ----------------------------------------------------------------------
@app.route('/create_new_recipe', methods = ['POST'])
def create_new_recipe():
    print(request.form)
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date' : request.form['date'],
        'thirty_minutes' : request.form['thirty_minutes'],
        'user_id' : session['user_id']
    }    
    Recipe.insert_row(data)
    return redirect('/dashboard')

# ----------------------------------------------------------------------
# One Single recipe Page
# ----------------------------------------------------------------------
@app.route('/recipes/<int:recipe_id>')
def recipe(recipe_id):
    recipe_data = {
        'id' : recipe_id
    }
    user_data = {
        'id' : session['user_id']
    }
    if("user_id" in session):
            user =  User.get_user_by_id(user_data)
            recipe = Recipe.get_recipe_by_id(recipe_data)
            return render_template('recipe.html', recipe=recipe, user=user)
    return redirect('/')

# ----------------------------------------------------------------------
# Edit One Single recipe Page
# ----------------------------------------------------------------------
@app.route('/recipes/edit/<int:recipe_id>')
def edit_one(recipe_id):
    recipe_data = {
        'id' : recipe_id
    }
    user_data = {
        'id' : session['user_id']
    }
    if("user_id" in session):
            user =  User.get_user_by_id(user_data)
            recipe = Recipe.get_recipe_by_id(recipe_data)
            return render_template('edit_recipe.html', recipe=recipe, user=user)
    return redirect('/')

@app.route('/update_recipe/<int:recipe_id>', methods = ["POST"])
def update_recipe(recipe_id):
    recipe_data = {
        'id' : recipe_id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date' : request.form['date'],
        'thirty_minutes' : request.form['thirty_minutes'],
        'user_id' : session['user_id']
    }
    result = Recipe.update_row(recipe_data)
    return redirect('/dashboard')



# ----------------------------------------------------------------------
# Delete recipe
# ----------------------------------------------------------------------
@app.route('/delete/<int:recipe_id>')
def delete(recipe_id):
    recipe_data = {
        'id' : recipe_id
    }
    Recipe.remove_recipe_by_id(recipe_data)
    return redirect('/dashboard')