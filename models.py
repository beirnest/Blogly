from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                    nullable=False)                 
    image = db.Column(db.Text, nullable=True)
    

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.String(),
                    nullable=False)    
    created_at = db.Column(db.DateTime(),
                    nullable=False)   
    user_id = db.Column(db.Integer,
                          db.ForeignKey('users.id'))
    user = db.relationship( 'User', backref='posts')

    