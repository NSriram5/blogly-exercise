from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users."""
    def setUp(self):
        """Add sample user data"""
        User.query.delete()
        weaving = User(first_name = 'Hugo',last_name = 'Weaving',image_url = "https://www.gstatic.com/tv/thumb/persons/27163/27163_v9_ba.jpg")
        fishburne = User(first_name = 'Laurence',last_name = 'Fishburne',image_url = "https://www.gstatic.com/tv/thumb/persons/71229/71229_v9_bb.jpg")
        foster = User(first_name = 'Gloria',last_name = 'Foster',image_url = "https://www.gstatic.com/tv/thumb/persons/157985/157985_v9_ba.jpg")
        mcclory = User(first_name = 'Belinda',last_name = 'McClory', image_url = "https://www.gstatic.com/tv/thumb/persons/249978/249978_v9_ba.jpg")

        db.session.add(weaving)
        db.session.add(fishburne)
        db.session.add(foster)
        db.session.add(mcclory)

        db.session.commit()

        self.id_to_test = weaving.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code,302)
            resp = client.get("/",follow_redirects=True)
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
