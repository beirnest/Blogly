"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


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

    return render_template("detail.html", user=user)

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