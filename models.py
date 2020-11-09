"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""
    __tablename__ = "user"

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

    created_posts = db.relationship('Post')

    def greet(self):
        """Greet using name."""
        return f"I'm {self.first_name} {self.last_name}"

    def get_full_name()
        """Method to generate a user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name()
        return f"{self.first_name} {self.last_name}"


    def __repr__(self):
        """Show info about the User"""
        p = self
        return f"<User {p.id} {p.first_name} {p.last_name}>"

Class Post(db.Model):
    """Posts"""
    __tablename__ = "post"

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
                    nullabe=False,
                    unique=False,
                    default=datetime.utcnow)
    created_by_user = db.Column(db.Integer,
                    db.ForeignKey('User.id'),
                    nullable=False)
    my_user = db.relationship('User')

    def __repr__(self):
        """Show details about the Post"""
        p = self
        return f"<Post {p.title} {p.created_at} {p.my_user}>"
