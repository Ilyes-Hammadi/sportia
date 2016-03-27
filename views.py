"""
    CODE HONOR
    this code is inspired by the Full Stack Foundations course so thanx udacity :)
"""

import json
import random
import string

import httplib2
import requests
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response
from flask import session as login_session
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Sport, User

#
# --------------------------------------------------- SETUP -------------------------------------------------------------
#

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('google_client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///sportia.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#
# ------------------------------------------------- HELPER METHODS ------------------------------------------------------
#


def json_responce(message, code):
    response = make_response(json.dumps(message, code))
    response.headers['Content-Type'] = 'application/json'
    return response


def create_user(login_session):
    user = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#
# ------------------------------------------------------ VIEWS ----------------------------------------------------------
#


@app.route('/login')
def login():
    """Create anti-forgery state token"""

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('user/login.html', login_session=login_session, STATE=state)


@app.route('/logout')
def logout():
    """This function logout the user acording to the intial login google+ or facebook"""

    if login_session['provider'] == "google":
        return redirect(url_for('gdisconnect'))
    elif login_session['provider'] == "facebook":
        return redirect(url_for('fbdisconnect'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """ Google plus connection """

    # Validate state token
    if request.args.get('state') != login_session['state']:
        return json_responce('Invalid state parameter.', 401)

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return json_responce('Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return json_responce(result.get('error'), 500)

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return json_responce("Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        return json_responce("Token's client ID does not match app's.", 401)

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return json_responce('Current user is already connected.', 200)

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # Get the user id if does exist
    user_id = get_user_id(login_session['email'])

    # If user does not exist create new one
    if not user_id:
        user_id = create_user(login_session)

    # Store the user id in the login session so that it can be user later
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """ Google plus disconnection """

    print login_session

    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']

    if access_token is None:
        print 'Access Token is None'
        return json_responce('Current user not connected.', 401)

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print 'result is '
    print result

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        flash('Successfully disconnected.')
        return redirect(url_for('categories'))
    else:

        return json_responce('Failed to revoke token for given user.', 400)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Facebook connection """

    if request.args.get('state') != login_session['state']:
        return json_responce('Invalid state parameter.', 401)

    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    #  logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    """ Facebook disconnection """

    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    del login_session['access_token']
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['provider']

    flash('Successfully disconnected.')
    return redirect(url_for('categories'))


@app.route('/')
@app.route('/categories')
@app.route('/categories/<int:category_id>')
def categories(category_id=None):
    """ Show all the categories according to the category id """

    # Get all the categories and sports from the database
    categories = session.query(Category).all()
    if category_id:
        try:
            sports = session.query(Sport).filter_by(category_id=category_id)
        except:
            pass
    else:
        sports = session.query(Sport).all()

    return render_template('categories/categories.html', login_session=login_session, categories=categories,
                           sports=sports, category_id=category_id)


@app.route('/category/new', methods=['GET', 'POST'])
def new_category():
    """ Add new category """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':

        # Get data from the front-end
        name = request.form['name']
        description = request.form['description']

        # Put the data into a model
        category = Category(name=name, user_id=login_session['user_id'])

        # Save description if there are one
        if description:
            category.description = description

        session.add(category)
        session.commit()

        return redirect(url_for('categories'))

    return render_template('categories/new_category.html')


@app.route('/category/<int:category_id>/update', methods=['GET', 'POST'])
def update_category(category_id):
    """ Update category """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')

    try:
        # Get the category with the id
        category = session.query(Category).get(category_id)

        # If the item was not found redirect to the home page
        if category == None:
            flash('Item does not exist')
            return redirect(url_for('categories'))

        # Check to see if the loged user is the owner of the item
        if login_session['user_id'] != category.user_id:
            flash("Your are not the owner of this item")
            return redirect(url_for('categories'))

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
            return render_template('categories/update_category.html', category=category)

    except:
        pass


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def delete_category(category_id):
    """ Delete category """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).get(category_id)

    # If the item was not found redirect to the home page
    if category == None:
        flash('Item does not exist')
        return redirect(url_for('categories'))

    # Check to see if the loged user is the owner of the item
    if login_session['user_id'] != category.user_id:
        flash("Your are not the owner of this item")
        return redirect(url_for('categories'))

    if request.method == 'POST':

        # Delete all the related items with the acctual category
        sports = session.query(Sport).filter_by(category_id=category.id)

        # Delete one by one
        for sport in sports:
            session.delete(sport)

        # Delete the category
        session.delete(category)

        # Commit all the changes
        session.commit()

        flash('Category deleted')
        return redirect(url_for('categories'))
    else:
        return render_template('categories/delete_category.html', category=category)


@app.route('/category/<int:category_id>/sport/<int:sport_id>')
def show_sport(category_id, sport_id):
    """ Show one sport """

    sport = None
    try:
        sport = session.query(Sport).get(sport_id)
    except:
        flash('This item does not exist')
        return redirect(url_for('categories'))
    return render_template('sport/show_sport.html', login_session=login_session, sport=sport)


@app.route('/sport/new/', methods=['GET', 'POST'])
def new_sport():
    """ New Sport """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        # Get the data from the request
        name = request.form['name']
        description = request.form['description']
        category_id = request.form['category_id']

        # Put the data into a model
        sport = Sport(name=name, category_id=category_id, user_id=login_session['user_id'])

        # if there are any description
        if description:
            sport.description = description

        session.add(sport)
        session.commit()

        return redirect(url_for('categories', category_id=category_id))
    else:
        # Check to see if there any categories in the database ohter wise we redirect the user
        # to create the first category
        categories = session.query(Category).all()

        if len(categories) == 0:
            flash('There no categoris create the first one please')
            return redirect(url_for('new_category'))

        return render_template('sport/new_sport.html', categories=categories)


@app.route('/category/<int:category_id>/sport/<int:sport_id>/update', methods=['GET', 'POST'])
def update_sport(category_id, sport_id):
    """ Update Sport """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')

    sport = None
    # Get the sport item from the database if it's exist
    try:
        sport = session.query(Sport).get(sport_id)

        # If the item was not found redirect to the home page
        if sport == None:
            flash('Item does not exist')
            return redirect(url_for('categories'))
    except:
        pass

    # Check to see if the loged user is the owner of the item
    if login_session['user_id'] != sport.user_id:
        flash("Your are not the owner of this item")
        return redirect(url_for('categories'))

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


@app.route('/category/<int:category_id>/sport/<int:sport_id>/delete', methods=['GET', 'POST'])
def delete_sport(category_id, sport_id):
    """ Delete Sport """

    # Check if the user is loged in
    if 'username' not in login_session:
        return redirect('/login')

    sport = session.query(Sport).get(sport_id)
    # If there no items redirect to the home page
    if sport == None:
        flash('This item does not exist')
        return redirect(url_for('categories'))

    # Check to see if the loged user is the owner of the item
    if login_session['user_id'] != sport.user_id:
        flash("Your are not the owner of this item")
        return redirect(url_for('categories'))

    if request.method == 'POST':
        session.delete(sport)
        session.commit()
        flash('Item deleted')
        return redirect(url_for('categories'))

    return render_template('sport/delete_sport.html', sport=sport)


#
# -------------------------------------------------- API ENDPOINT -------------------------------------------------------
#


@app.route('/api/users')
def users_json():
    """ Return the all the users data in json format """

    users = session.query(User).all()
    return jsonify(users=[user.serialize for user in users])


@app.route('/api/categories')
def categories_json():
    """ Return all the categories data in json format """

    categories = session.query(Category).all()
    return jsonify(categories=[category.serialize for category in categories])


@app.route('/api/sports')
def sports_json():
    """ Return all the sports data in json format """

    sports = session.query(Sport).all()
    return jsonify(sports=[sport.serialize for sport in sports])


@app.route('/api/user/<int:user_id>')
def user_json(user_id):
    """ Return user data in json format accordin to the user_id param"""

    user = session.query(User).get(user_id)
    return jsonify(user.serialize)


@app.route('/api/category/<int:category_id>')
def category_json(category_id):
    """ Return category data in json format accordin to the category_id param"""

    try:
        category = session.query(Category).get(category_id)
        return jsonify(category.serialize)
    except:
        return jsonify({'message': 'does not exist'})


@app.route('/api/sport/<int:sport_id>')
def sport_api(sport_id):
    """ Return sport data in json format accordin to the sport_id param"""

    try:
        sport = session.query(Sport).get(sport_id)
        return jsonify(sport.serialize)
    except:
        return jsonify({'message': 'does not exist'})
