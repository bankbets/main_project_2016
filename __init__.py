from flask import Flask, render_template, session, redirect, request, flash, jsonify, url_for
from database import connection, register, checkUser, checkLogin
import os
from MySQLdb import escape_string as escaper

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return redirect('/')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = escaper(request.form['username'])
    pass1 = escaper(request.form['pass1'])
    email = escaper(request.form['email'])
    if(len(username) < 3):
        return "short"
    if checkUser(username, email):
        return "taken"
    if register(username, pass1, email):
        return "done"
    return "fail"

@app.route('/check_login', methods=['POST'])
def check_login():
    username = escaper(request.form['userlogin'])
    pass1 = escaper(request.form['userpass'])
    print("CHECKING " + str(username) + str(pass1))
    if checkLogin(username, pass1):
        session.clear()
        session['user'] = username
        return "login"
    return "fail"

if __name__ == "__main__":
    app.run()