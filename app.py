from flask import Flask, request, render_template, session, make_response, redirect, flash, jsonify
from random import choice, randint
from unittest import TestCase
from flask_debugtoolbar import DebugToolbarExtension
from currency import CurrencyMethods

app = Flask(__name__)

app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False 
# app.config["TESTING"] = True
# app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

debug = DebugToolbarExtension(app)

currency_method = CurrencyMethods()

@app.route('/')
def home_page():
    """shows home page"""  

    return render_template("index.html")

@app.route('/response', methods=["POST"])
def result_page():
    """shows currency exchange rate"""
    
    start_curr = request.form["converting-from"].upper()
    end_curr = request.form["converting-to"].upper()
    amount = request.form["amount"]

    currency_method.checking_converting_from(start_curr)
    
    end_symbol = currency_method.checking_converting_to(end_curr)

    currency_method.checking_amount_validity(amount)

    rounded = currency_method.checking_all(start_curr, end_curr, amount)       

    return render_template("response.html", rounded=rounded, end_symbol=end_symbol)

