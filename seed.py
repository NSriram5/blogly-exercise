from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

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

# Commit to save the changes to the database
db.session.commit()