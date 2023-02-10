"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
def show_user(user_id):
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
    tags = Tag.query.all()
    return render_template("add_post.html", user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add Post"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    current_time = datetime.datetime.now()
    tags = request.form.getlist('tag')

    post = Post(title = title, content = content, created_at = current_time, user_id = user.id)
    db.session.add(post)
    db.session.commit()

    for tag in tags:
        tag_info = Tag.query.get(tag)
        post_info = db.session.query(Post).order_by(Post.id.desc()).first()
        post_tag = PostTag(post_id = post_info.id, tag_id = tag_info.id)
        db.session.add(post_tag)
        db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def load_post(post_id):
    """Load a post by id"""
    post = Post.query.get_or_404(post_id)
    tags = post.tag
    return render_template("post.html", post = post, tags = tags)

@app.route('/posts/<int:post_id>/edit')
def load_edit_post(post_id):
    """View post edit page"""
    post = Post.query.get_or_404(post_id)
    tags = post.tag
    all_tags = Tag.query.all()
    return render_template("edit_post.html", post = post, tags = tags, all_tags = all_tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def save_edit_post(post_id):
    """Save post edit"""
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

@app.route('/tags')
def load_tags():
    tags = Tag.query.all()
    
    return render_template("tag.html", tags = tags)

@app.route('/tags/<int:tag_id>')
def load_tag(tag_id):
    """Load tag details by id"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", tag = tag, posts = posts)

@app.route('/tags/new')
def new_tag():
    """Load page to add new tag"""

    return render_template("new_tag.html")

@app.route('/tags/new', methods=["POST"])
def add_new_tag():
    """Add new tag and redirect to Tags page"""

    name = request.form['tag_name']

    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def load_edit_tag(tag_id):
    """Load edit tag page"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def save_edit_tag(tag_id):
    """Save tag edit"""

    name = request.form['tag_name']

    tag = Tag.query.get_or_404(tag_id)

    tag.name = name
    db.session.commit()

    return render_template("tag_details.html", tag = tag)

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')



