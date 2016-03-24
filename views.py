import flask

app = flask.Flask(__name__)


# Show all categories
@app.route('/')
@app.route('/categories')
def categories():
    return 'Show all categories'


# Add new category
@app.route('/category/new')
def new_category():
    return 'Add category'


# Update category
@app.route('/category/<int:category_id>/update')
def update_category(category_id):
    return 'Update category id : %s' % category_id


# Delete category
@app.route('/category/<int:category_id>/delete')
def delete_category(category_id):
    return 'Delete category id : %s' % category_id


# Show one sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>')
def show_sport(category_id, sport_id):
    return 'Show sport id %s category %s' % (sport_id, category_id)


# New Sport
@app.route('/sport/new')
def new_sport():
    return 'New Sport'


# Update Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/update')
def update_sport(category_id, sport_id):
    return 'Update sport id %s category %s' % (sport_id, category_id)


# Delete Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/delete')
def delte_sport(category_id, sport_id):
    return 'Delete sport id %s category %s' % (sport_id, category_id)
