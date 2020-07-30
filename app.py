from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify
from random import choice, randint
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

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

    return render_template("details.html", user=user)

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
    
    # User.query.get(user_id).delete()
    User.query.filter_by(id=user_id).delete()
  
    db.session.commit()

    return redirect("/")


# @app.route('/')
# def home_page():
#     """shows home page"""  

#     return render_template("index.html")

# @app.route('/response', methods=["POST"])
# def result_page():
#     """shows currency exchange rate"""
    
#     start_curr = request.form["converting-from"].upper()
#     end_curr = request.form["converting-to"].upper()
#     amount = request.form["amount"]

#     currency_method.checking_converting_from(start_curr)
    
#     end_symbol = currency_method.checking_converting_to(end_curr)

#     currency_method.checking_amount_validity(amount)

#     rounded = currency_method.checking_all(start_curr, end_curr, amount)       

#     return render_template("response.html", rounded=rounded, end_symbol=end_symbol)

