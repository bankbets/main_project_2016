import MySQLdb
from MySQLdb import escape_string as escaper
import hashlib, uuid
import datetime
import time

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="sushitomipizza!(", db="bank_bets")
    c = conn.cursor()
    return c, conn

def register(username, pass1, email):
    c, conn = connection()
    salt = uuid.uuid4().hex
    password = hashlib.sha512(str(pass1) + salt).hexdigest()
    c.execute("INSERT INTO member_accounts (username, email, password, salt, type, balance) VALUES (%s, %s, %s, %s, 'M', 0)", (escaper(username), escaper(email), escaper(password), escaper(salt)))
    conn.commit()
    conn.close()
    return True

def checkUser(user, email):
    c, conn = connection()

    x = c.execute("SELECT * FROM member_accounts WHERE username=(%s) OR email=(%s)", (user, email))
    if int(x) > 0:
        conn.close()
        return True
    conn.close()
    return False

def getUserId(user):
    c, conn = connection()
    x = c.execute("SELECT personID FROM member_accounts WHERE username = (%s)", [escaper(user)])
    if int(x) == 0:
        return -1
    data = c.fetchone()
    conn.close()
    return data[0]

def checkLogin(username, pass1):
    c, conn = connection()
    x = c.execute("SELECT * FROM member_accounts WHERE username = (%s)", [escaper(username)])
    if int(x) == 0:
        conn.close()
        return False
    else:
        datalogin = c.fetchone()
        print(datalogin)
        hashed_pass = hashlib.sha512(str(pass1) + datalogin[4]).hexdigest()
        if(str(hashed_pass) != datalogin[3]):
            return False
        else:
            return True

def getBalance(user):
    if user == 'OFFLINE1111111111111111111111111111111111111111111111':
        return 0
    c, conn = connection()
    x = c.execute("SELECT balance FROM member_accounts WHERE username= (%s)", [escaper(user)])
    if int(x) == 0:
        conn.close()
        return 0
    else:
        datalogin = c.fetchone()
        conn.close()
        return datalogin[0]

def requestDeposit(user, game_type, amount):
    c, conn = connection()
    userid = getUserId(user)
    requester_key = "D" + uuid.uuid4().hex
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO deposit_requests (personID, amount, request_key, game_type, date_time, status) VALUES (%s, %s, %s, %s, %s, 'Open')", [int(userid), escaper(amount), escaper(requester_key), str(st), escaper(game_type)])
    conn.commit()
    conn.close()
    return requester_key

def requestWithdraw(user, game_type, amount):
    c, conn = connection()
    userid = getUserId(user)
    requester_key = "W" + uuid.uuid4().hex
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO withdraw_requests (personID, amount, request_key, game_type, date_time, status) VALUES (%s, %s, %s, %s, %s, 'Open')", [int(userid), escaper(amount), escaper(requester_key), str(st), escaper(game_type)])
    conn.commit()
    conn.close()
    return requester_key

def getPreviousRequests(user):
    if user == 'OFFLINE1111111111111111111111111111111111111111111111':
        return []
    else:
        c, conn = connection()
        userid = getUserId(user)
        x = c.execute("SELECT * FROM deposit_requests WHERE personID=%s", [int(userid)])
        if int(x) == 0:
            return []
        allRequests = []
        row = c.fetchone()
        while row is not None:
            currRequest = dict(game=row[3], date=row[2], key=row[4], amt=row[1], status=row[5])
            allRequests.append(currRequest)
            row = c.fetchone()
        c.close()
        conn.close()
        print(allRequests)
        return allRequests
