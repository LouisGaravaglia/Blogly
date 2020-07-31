from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify
from random import choice, randint
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
# app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

connect_db(app)

debug = DebugToolbarExtension(app)




@app.route('/')
def home_page():
    """shows lists of all users in db"""  
    
    users = User.query.all()

    return render_template("index.html", users=users)



@app.route('/<int:user_id>')
def show_user(user_id):
    """shows details page about a single user"""  
    
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Pet.owner_id == user_id).all() 

    return render_template("details.html", user=user, posts=posts)

@app.route('/create_user')
def create_user_page():
    """shows the form to input info and create a user"""  
    

    return render_template("create_user.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    """use a form to create a user"""  
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
   
    
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")

@app.route('/<int:user_id>/edit')
def edit_user_page(user_id):
    """shows the form to edit an existing user"""  
    
    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)

@app.route('/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """use a form to update and edit a user"""  
    user = User.query.get_or_404(user_id)
    
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
   
    
    # new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")


@app.route('/<int:user_id>/delete')
def delete_user(user_id):
    """delete a user from the database"""  
    
    
    User.query.filter_by(id=user_id).delete()
  
    db.session.commit()

    return redirect("/")


@app.route('/<int:user_id>/add_post')
def add_post_page(user_id):
    """shows the form to add a post"""  
    
    user = User.query.get_or_404(user_id)

    return render_template("add_post.html", user=user)

@app.route('/<int:user_id>/add_post', methods=["POST"])
def create_post(user_id):
    """use a form to create a user"""  
    
    title = request.form["title"]
    content = request.form["content"]
    
    user = User.query.get_or_404(user_id)
   
    
    new_post = Post(title=title, content=content, owner_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/{user.id}")