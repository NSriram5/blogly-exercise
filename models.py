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