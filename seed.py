from models import User, Post, Tag, db
from app import app
from datetime import datetime

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add Users
weaving = User(first_name = 'Hugo',last_name = 'Weaving',image_url = "https://www.gstatic.com/tv/thumb/persons/27163/27163_v9_ba.jpg")
fishburne = User(first_name = 'Laurence',last_name = 'Fishburne',image_url = "https://www.gstatic.com/tv/thumb/persons/71229/71229_v9_bb.jpg")
foster = User(first_name = 'Gloria',last_name = 'Foster',image_url = "https://www.gstatic.com/tv/thumb/persons/157985/157985_v9_ba.jpg")
mcclory = User(first_name = 'Belinda',last_name = 'McClory', image_url = "https://www.gstatic.com/tv/thumb/persons/249978/249978_v9_ba.jpg")

# Add new objects to session, so they'll persist
db.session.add(weaving)
db.session.add(fishburne)
db.session.add(foster)
db.session.add(mcclory)

# Add Posts
dt_stamp = datetime(year = 2020,month = 11,day  = 9, hour = 13,minute = 55,second = 23)
weaving = User.query.filter(User.first_name == "Hugo").first()
first = Post(title = "First post",content = "Wowee the very first post I hope no one inter-",created_at = dt_stamp,created_by_user = weaving.id)
dt_stamp = datetime(year = 2020,month = 11,day  = 9, hour = 13,minute = 55,second = 50)
foster = User.query.filter(User.first_name == "Gloria").first()
second = Post(title = "Second post",content = "yesss I get to be second!",created_at = dt_stamp,created_by_user = foster.id)

# Add Tags
sunshine = Tag(name = 'sunshine')
rainbows = Tag(name = 'rainbows')

db.session.add(sunshine)
db.session.add(rainbows)

db.session.add(first)
db.session.add(second)

# Commit to save the changes to the database
db.session.commit()