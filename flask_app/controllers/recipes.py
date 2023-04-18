from flask_app import app, render_template, redirect, request, session 
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

#! CREATE
@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes/new.html', users = User.get_all())

@app.route('/create', methods=['post'])
def create():
    if not Recipe.validate_recipe(request.form):
        return redirect('/new')
    Recipe.save(request.form)
    return redirect('/recipes')

#! READ ALL
@app.route('/recipes')        
def recipes():
    if 'user_id' not in session:
        return redirect('/')
    recipes = Recipe.get_all()
    print(recipes)
    return render_template('recipes/index.html', recipes = recipes) 

#! READ ONE
@app.route('/recipes/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_recipe(id)
    print(recipe)
    return render_template('recipes/show.html', recipe = recipe)


#! UPDATE

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes/edit.html', recipe = Recipe.get_recipe(id))

@app.route('/update', methods=['post'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")
    Recipe.update(request.form)
    return redirect('/recipes')

#! DELETE 
@app.route('/recipes/delete/<int:id>')
def destroy(id):
    data = {'id': id}
    Recipe.delete(id)
    return redirect('/recipes')