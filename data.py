#
#--------------------- SETUP FAKE DATA --------------------
#

# Setup the database with some fake data
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, User, Sport

categories_json = json.loads(open('data.json').read())['categories']
sports_json = json.loads(open('data.json').read())['sports']

# Connect to Database and create database session
engine = create_engine('sqlite:///sportia.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


categories = []
sports = []

# Create the first user
session.add(User(name='tux', email='tux@tux.com',
                 picture='https://openclipart.org/image/2400px/svg_to_png/193554/cyberscooty-tux-graduate.png'))

user = session.query(User).filter_by(email='tux@tux.com')[0]

for c in categories_json:
    categories.append(Category(name=c['name'], description=c['description'], user_id=user.id))

for c in categories:
    session.add(c)
    session.commit()

for s in sports_json:
    sports.append(Sport(name=s['name'], description=s['description'], category_id=s['category_id'], user_id=user.id))

for s in sports:
    session.add(s)
    session.commit()
