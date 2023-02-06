"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import datetime


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def landing_page():
    """Load Home page"""
    
    return redirect('/users')

@app.route('/users')
def load_users():
    """Load User List"""   
    users = User.query.all()
    
    return render_template("base.html", users = users)

@app.route('/users/new')
def new_users():
    """Load New User Page"""

    return render_template("new_user.html")

@app.route('/users/new', methods=["POST"])
def add_user():
    """Process new user form and add user to database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name = first_name, last_name = last_name, image = img_url)
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_use(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id)

    return render_template("detail.html", user=user, posts = posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """View Edit User Details page"""
    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def save_edit(user_id):
    """Save edited changes to user"""
    user = User.query.get_or_404(user_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user.first_name = first_name
    user.last_name = last_name
    user.image = img_url
    db.session.commit()

    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit() 

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def load_add_post(user_id):
    """Load Add Post page"""
    user = User.query.get_or_404(user_id)
    return render_template("add_post.html", user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add Post"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    current_time = datetime.datetime.now()

    post = Post(title = title, content = content, created_at = current_time, user_id = user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def load_post(post_id):
    """Load a post by id"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post = post)

@app.route('/posts/<int:post_id>/edit')
def load_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def save_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']

    post.title = title
    post.content = content
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a user"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit() 

    return redirect(f"/users/{user_id}")

