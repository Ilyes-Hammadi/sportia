from flask import Flask, render_template

app = Flask(__name__)


# Show all categories
@app.route('/')
@app.route('/categories')
def categories():
    return render_template('categries/categories.html')


# Add new category
@app.route('/category/new')
def new_category():
    return render_template('categries/new_category.html')


# Update category
@app.route('/category/<int:category_id>/update')
def update_category(category_id):
    return render_template('categries/update_category.html')


# Delete category
@app.route('/category/<int:category_id>/delete')
def delete_category(category_id):
    return render_template('categries/delete_category.html')


# Show one sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>')
def show_sport(category_id, sport_id):
    return render_template('sport/show_sport.html')


# New Sport
@app.route('/sport/new')
def new_sport():
    return render_template('sport/new_sport.html')


# Update Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/update')
def update_sport(category_id, sport_id):
    return render_template('sport/update_sport.html')


# Delete Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/delete')
def delte_sport(category_id, sport_id):
    return render_template('sport/delete_sport.html')
