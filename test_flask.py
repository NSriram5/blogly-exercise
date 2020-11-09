from unittest import TestCase

from app import app
from models import db, User, Post

from datetime import datetime

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']



class UserViewsTestCase(TestCase):
    """Tests for views for users."""
    def setUp(self):
        """Add sample user data"""

        db.drop_all()
        db.create_all()

        # If table isn't empty, empty it
        User.query.delete()
        Post.query.delete()

        weaving = User(first_name = 'Hugo',last_name = 'Weaving',image_url = "https://www.gstatic.com/tv/thumb/persons/27163/27163_v9_ba.jpg")
        fishburne = User(first_name = 'Laurence',last_name = 'Fishburne',image_url = "https://www.gstatic.com/tv/thumb/persons/71229/71229_v9_bb.jpg")
        foster = User(first_name = 'Gloria',last_name = 'Foster',image_url = "https://www.gstatic.com/tv/thumb/persons/157985/157985_v9_ba.jpg")
        mcclory = User(first_name = 'Belinda',last_name = 'McClory', image_url = "https://www.gstatic.com/tv/thumb/persons/249978/249978_v9_ba.jpg")

        db.session.add(weaving)
        db.session.add(fishburne)
        db.session.add(foster)
        db.session.add(mcclory)

        db.session.commit()

        self.id_to_test = User.query.filter_by(first_name = "Hugo").first().id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("<div class=\"h2 m-3\">\n    Active Users\n</div>",html)

    def test_show_hugo(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id_to_test}")
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('<div class=\"h3\">Hugo Weaving</div>',html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"firstName":"hello","lastName":"there","imageUrl":""}
            resp = client.post("/users/new",data=data,follow_redirects=True)
            html =resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("<a href=\"users/5\">hello there</a>",html)

    def test_delete_hugo(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.id_to_test}/delete",follow_redirects=True)
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertNotIn('<div class=\"h3\">Hugo Weaving</div>',html)


class PostViewsTestCase(TestCase):
    """Tests for views for users."""
    def setUp(self):
        """Add sample user data"""
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

        db.session.add(first)
        db.session.add(second)

        # Commit to save the changes to the database
        db.session.commit()

        self.id_to_test = User.query.filter_by(first_name = "Hugo").first().id

        self.post_to_test = Post.query.filter_by(title = "Second post").first().id

    def tearDown(self):
        db.session.rollback()
    def test_posts_on_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Wowee the very",html)
    
    def test_show_hugo(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id_to_test}")
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('First post',html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_to_test}")
            html = resp.get_data(as_text = True)
            self.assertEqual(resp.status_code,200)
            self.assertIn('yesss I get to be second',html)
