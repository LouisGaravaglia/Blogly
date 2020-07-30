from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify
from random import choice, randint
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from currency import CurrencyMethods
from models import db, connect_db

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

currency_method = CurrencyMethods()


@app.route('/')
def home_page():
    """shows index page"""  
    
    pets = Pet.query.all()

    return render_template("list.html", pets=pets)

@app.route('/<int: pet_id>')
def show_details():
    """shows details about a single pet"""  
    
    pet = Pet.query.get(pet_id)

    return render_template("details.html", pet=pet)



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

