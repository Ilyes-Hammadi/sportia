from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Sport

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///sportia.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all categories
@app.route('/')
@app.route('/categories')
@app.route('/categories/<int:category_id>')
def categories(category_id=None):
    # Get all the categories and sports from the database
    categories = session.query(Category).all()
    if category_id:
        try:
            sports = session.query(Sport).filter_by(category_id=category_id)
        except:
            pass
    else:
        sports = session.query(Sport).all()

    return render_template('categries/categories.html', categories=categories, sports=sports)


# Add new category
@app.route('/category/new', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':

        # Get data from the front-end
        name = request.form['name']
        description = request.form['description']

        # Put the data into a model
        category = Category(name=name)

        # Save description if there are one
        if description:
            category.description = description

        session.add(category)
        session.commit()

        return redirect(url_for('categories'))

    return render_template('categries/new_category.html')


# Update category
@app.route('/category/<int:category_id>/update', methods=['GET', 'POST'])
def update_category(category_id):
    # Get the category with the id
    category = session.query(Category).get(category_id)

    # if it's a POST request
    if request.method == 'POST':
        category.name = request.form['name']

        # if there a description
        if request.form['description']:
            category.description = request.form['description']

        # save the changes into the database
        session.add(category)
        session.commit()

        # redirect the user to the categories page
        return redirect(url_for('categories'))

    else:
        return render_template('categries/update_category.html', category=category)


# Delete category
@app.route('/category/<int:category_id>/delete')
def delete_category(category_id):
    category = session.query(Category).get(category_id)
    session.delete(category)
    session.commit()
    return render_template('categries/delete_category.html')


# Show one sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>')
def show_sport(category_id, sport_id):
    sport = None
    try:
        sport = session.query(Sport).get(sport_id)
    except:
        pass
    return render_template('sport/show_sport.html', sport=sport)


# New Sport
@app.route('/sport/new/', methods=['GET', 'POST'])
def new_sport():
    if request.method == 'POST':
        # Get the data from the request
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']

        # Put the data into a model
        sport = Sport(name=name, category_id=category_id)

        # if there are any description
        if description:
            sport.description = description

        session.add(sport)
        session.commit()

        return redirect(url_for('categories', category_id=category_id))
    else:
        categories = session.query(Category).all()
        return render_template('sport/new_sport.html', categories=categories)


# Update Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/update', methods=['GET', 'POST'])
def update_sport(category_id, sport_id):
    sport = None
    # Get the sport item from the database if it's exist
    try:
        sport = session.query(Sport).get(sport_id)
    except:
        pass

    # If the request is a POST request validate and save the data
    if request.method == 'POST':
        # Get the data from the request
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']

        # Put the data into a model
        sport.name = name
        sport.category_id = category_id

        # if there are any description
        if description:
            sport.description = description

        session.add(sport)
        session.commit()

        return redirect(url_for('categories', category_id=category_id))
    else:
        categories = session.query(Category).all()
        return render_template('sport/update_sport.html', sport=sport, categories=categories)


# Delete Sport
@app.route('/category/<int:category_id>/sport/<int:sport_id>/delete')
def delte_sport(category_id, sport_id):

    try:
        sport = session.query(Sport).get(sport_id)
        session.delete(sport)
        session.commit()
    except:
        pass

    return render_template('sport/delete_sport.html')
