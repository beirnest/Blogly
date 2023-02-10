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
    tag = db.relationship('Tag',
                               secondary='post_tags',
                               backref='posts')

class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)

class PostTag(db.Model):
    """PostTag"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,
                   db.ForeignKey('posts.id'),
                   primary_key=True)
    tag_id = db.Column(db.Integer,
                   db.ForeignKey('tags.id'),
                   primary_key=True)            
    db.ForeignKeyConstraint(['post_id','tag_id'],['posts.id', 'tags.id'])



    