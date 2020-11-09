"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class Post(db.Model):
    """Posts"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    content = db.Column(db.String(250),
                    nullable=False,
                    unique=False)
    created_at = db.Column(db.DateTime,
                    nullable=False,
                    unique=False,
                    default=datetime.utcnow())
    created_by_user = db.Column(db.Integer,
                    db.ForeignKey('users.id'),
                    nullable=False)
    my_user = db.relationship('User',backref='post')

    def __repr__(self):
        """Show details about the Post"""
        p = self
        return f"<Post {p.title} {p.created_at} {p.my_user}>"

class User(db.Model):
    """Users"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    last_name = db.Column(db.String(50),
                    nullable=False,
                    unique=False)
    image_url = db.Column(db.String(100),
                    nullable=True,
                    unique=False)

    created_posts = db.relationship('Post',backref='user',cascade="all, delete-orphan")

    def greet(self):
        """Greet using name."""
        return f"I'm {self.first_name} {self.last_name}"

    def get_full_name(self):
        """Method to generate a user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __repr__(self):
        """Show info about the User"""
        p = self
        return f"<User {p.id} {p.first_name} {p.last_name}>"


