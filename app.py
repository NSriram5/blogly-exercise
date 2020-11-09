"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "12345"
debug = DebugToolbarExtension(app)

#import seed

@app.route("/")
def root():
    """redirect to list of users for now"""
    return redirect("/users")

@app.route("/users")
def list_users():
    """List users and include buttons to detail and add views."""
    users = User.query.order_by(User.last_name).all()
    return render_template("list_users.html",users=users)

@app.route("/users/new",methods=["POST","GET"])
def add_user():
    """Show the add user create form"""
    if request.method == "GET":
        return render_template("create_user.html")
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageUrl']
    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html",user = user, posts = user.created_posts)

@app.route("/users/<int:user_id>/edit",methods=["POST","GET"])
def modify_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method =="GET":
        first_name = user.first_name
        last_name = user.last_name
        image_url = user.image_url
        user_id = user.id
        return render_template("modify_user.html",user_id = user_id, first_name = first_name, last_name = last_name, image_url = image_url)
    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imageUrl']
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete",methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new",methods=["POST","GET"])
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "GET":
        return render_template("create_post.html",userid = user_id, full_name = user.full_name)
    title = request.form['title']
    postcontent = request.form['postcontent']
    post = Post(title = title, content = postcontent)
    id = post.id
    db.session.add(user)
    db.session.commit()
    return redirect(f"/posts/{id}")

#
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    username = post.my_user.full_name
    user_id = post.my_user.id
    return render_template("show_post.html",post = post, full_name = full_name, user_id = user_id)

#
@app.route("/posts/<int:post_id>/edit",methods=["POST","GET"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        return render_template("editPost.html",post = post)
    post.title = request.form['title']
    post.content = request.form['postcontent']
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')
    return redirect("/")