from flask import Flask, render_template, session, redirect, request, flash, jsonify, url_for
from database import connection, register, checkUser, checkLogin, getBalance, requestDeposit, requestWithdraw, getPreviousRequests, isAdmin, getPendingDeposits, getInfoOnKey, makeDeposit, getPendingWithdraws, makeWithdrawl
import os
from dice import roll
from MySQLdb import escape_string as escaper

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('index.html', loggedinstatus=getLogIn(), loggedinli=getLogInLi())

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dice')
def dice():
    return render_template('dice.html', loggedin=getLogInStatus(), balanceacc=getBalance(getUser()), loggedinli=getLogInLi())


@app.route('/cashier')
def cashier():
    return render_template('cashier.html', loggedin=getLogInStatus(), loggedinli=getLogInLi(), balanceacc=getBalance(getUser()), previous_requests = getPreviousRequests(getUser()))

@app.route('/request_deposit', methods=['POST'])
def request_deposit():
    if getLogInStatus():
        game_type = escaper(request.form['game_type'])
        amount = escaper(request.form['amount'])
        if game_type[0] == 'O' or game_type[0] == 'o':
            type = "Old School"
        else:
            type = "RS3"
        unique_deposit = requestDeposit(getUser(), type, amount)
        return render_template('requested.html', request_id=unique_deposit, loggedin=getLogInStatus(), type_request='deposit', game_type = type, requested_gold = amount)
    else:
        return redirect('/')

@app.route('/admin/submit_Deposit', methods=['POST'])
def submit_deposit():
    if getLogInStatus():
        if isAdmin(session['user']) == True:
            depkey = request.form['depkey']
            depuser = request.form['depuser']
            amt = request.form['deposit_amt']
            type = request.form['game_type']
            rsname = request.form['rs_name']
            makeDeposit(depkey, depuser, amt, type, getUser(), rsname)
            return redirect('/admin/manage')
        else:
            return render_template('404.html')
    else:
        return redirect('/')

@app.route('/request_withdraw', methods=['POST'])
def request_withdraw():
    if getLogInStatus():
        game_type = escaper(request.form['game_type'])
        amount = escaper(request.form['amount'])
        if game_type[0] == 'O' or game_type[0] == 'o':
            type = "Old School"
        else:
            type = "RS3"
        unique_deposit = requestWithdraw(getUser(), type, amount)
        return render_template('requested.html', request_id=unique_deposit, loggedin=getLogInStatus(),
                               type_request='withdrawl', game_type=type, requested_gold=amount)
    else:
        return redirect('/')

@app.route('/admin/submit_Withdrawl', methods=['POST'])
def submit_withdrawl():
    if getLogInStatus():
        if isAdmin(session['user']) == True:
            depkey = request.form['depkey']
            depuser = request.form['depuser']
            amt = request.form['deposit_amt']
            type = request.form['game_type']
            rsname = request.form['rs_name']
            makeWithdrawl(depkey, depuser, amt, type, getUser(), rsname)
            return redirect('/admin/manage')
        else:
            return render_template('404.html')
    else:
        return redirect('/')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/grab_info/<item>/<t>', methods=['GET'])
def grab_info(item, t):
    key = item
    if t == 'd':
        allInfo = getInfoOnKey(key, getUser(), 'd')
        thisType = "Deposit"
    else:
        allInfo = getInfoOnKey(key, getUser(), 'w')
        thisType = "Withdrawl"
    return render_template("deposit_request.html", item = allInfo, type = thisType)

@app.route('/admin')
def admin_page():
    if getLogInStatus() == False:
        return render_template('404.html')
    if isAdmin(session['user']) == False:
        return render_template('404.html')
    return render_template('admin.html', notify = 0, pic = 'admin', username = getUser())

@app.errorhandler(404)
def error404(e):
    return render_template('404.html')

@app.route('/admin/manage')
def admin_manage():
    if getLogInStatus() == False:
        return render_template('404.html')
    if isAdmin(session['user']) == False:
        return render_template('404.html')
    user = getUser()
    return render_template('manage_accounts.html', notify = 0, pic = 'admin', username = user, pendingdeposits = getPendingDeposits(user), pendingwithdraws = getPendingWithdraws(user))

def getLogIn():
    if 'user' not in session:
        return ""
    return "display: none;"

def getLogInLi():
    if 'user' not in session:
        return '<li><a href="#" id="display_login">Login</a></li>'
    return '<li><a href="/logout" id="logout_">Logout (' + session['user'] + ')</a></li><li><a href="#">Balance: ' + str(getBalance(session['user'])) + ' Tokens</a></li>'

def getLogInStatus():
    if 'user' not in session:
        return False
    return True

def getUser():
    if 'user' not in session:
        return 'OFFLINE1111111111111111111111111111111111111111111111'
    else:
        return session['user']

if __name__ == "__main__":
    app.run()