from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify
from random import choice, randint
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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


# ===================================    HOME    =====================================


@app.route('/')
def home_page():
    """shows lists of all users in db"""  
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("index.html", posts=posts)


# ===================================    USER PAGE / USERS    =====================================


@app.route('/<int:user_id>')
def show_user(user_id):
    """shows details page about a single user"""  
    
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.owner_id == user_id).all() 

    return render_template("details.html", user=user, posts=posts)

@app.route('/users')
def show_users():
    """shows list of all users"""  
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    # users = Post.query.filter(Post.owner_id == 1).all()

    return render_template("users.html", users=users)


# ===================================    CREATE USER    =====================================


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

# ===================================    EDIT/DELETE USER    =====================================


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
   
    
    
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")


@app.route('/<int:user_id>/delete')
def delete_user(user_id):
    """delete a user from the database"""  
    
    
    User.query.filter_by(id=user_id).delete()
  
    db.session.commit()

    return redirect("/")

# ===================================    ADD POSTS    =====================================

@app.route('/<int:user_id>/add_post')
def add_post_page(user_id):
    """shows the form to add a post"""  
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("add_post.html", user=user, tags=tags)

@app.route('/<int:user_id>/add_post', methods=["POST"])
def create_post(user_id):
    """use a form to create a user"""  
    
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
   

    return redirect(f"/{user.id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show the post when user clicks on the post title"""  
    
    
    post = Post.query.get_or_404(post_id)
    # tags_ids = PostTag.query.filter_by(post_id=post_id).all()
    # tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
   
    

    return render_template("show_post.html", post=post)


# ===================================    EDIT/DELETE POSTS    =====================================



@app.route('/posts/<int:post_id>/edit_post')
def show_edit_post_page(post_id):
    """shows the form to edit an existing post"""  
    
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    
    
    

    return render_template("edit_post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit_post', methods=["POST"])
def edit_user_post(post_id):
    """use a form to update and edit a post""" 

    post = Post.query.get_or_404(post_id)

    if request.form["title"] != "" and request.form["title"] !=  None:
        post.title = request.form["title"]
    
            
    if request.form["content"] != "" and request.form["content"] != None:
        post.content = request.form["content"]
    
   
    db.session.add(post)
    db.session.commit()
    
    # ////////////////////// TOD0: NEED TO ADD THE UNCHECKING OF TAGS
    
        tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()
    
# ////////////////////// TOD0: NEED TO ADD THE UNCHECKING OF TAGS ABOVE

    

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete_post')
def delete_user_post(post_id):
    """delete a post from the database"""  
    
    
    Post.query.filter_by(id=post_id).delete()
  
    db.session.commit()

    return redirect("/")

# ===================================    CREATE TAGS    =====================================

@app.route('/create_tag')
def show_create_tag_page():
    """shows the form to create a tag to then add to posts."""  
    
    tags = Tag.query.all()

    return render_template("create_tag.html", tags=tags)

@app.route('/create_tag', methods=["POST"])
def create_tag_post():
    """use a form to create a tag and update the tag db."""  
    
    
    tag_name = request.form['tag_name']
    

    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()
   

    return redirect("/create_tag")