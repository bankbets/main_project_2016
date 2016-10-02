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

def isAdmin(user):
    c, conn = connection()
    userid = getUserId(user)
    x = c.execute("SELECT type FROM member_accounts WHERE personID= (%s)", [int(userid)])
    if int(x) == 0:
        return False
    row = c.fetchone()
    if row[0] == "A":
        return True
    return False

def getPendingDeposits(user):
    if isAdmin(user):
        c, conn = connection()
        x = c.execute("SELECT a.*, b.username FROM deposit_requests a JOIN member_accounts b WHERE a.status='Open' AND a.personID = b.personID")
        row = c.fetchone()
        allReqs = []
        while row is not None:
            closeup = "<button type='button' onclick='openReq(\"" + row[4] + "\")'>Fulfill</button>"
            currReq = dict(game=row[3], date=row[2], key=row[4], amt=row[1], status=row[5], requestuser=row[6], closeup=closeup)
            allReqs.append(currReq)
            row = c.fetchone()
        c.close()
        conn.close()
        return allReqs
    else:
        return []

def getPendingWithdraws(user):
    if isAdmin(user):
        c, conn = connection()
        x = c.execute("SELECT a.*, b.username FROM withdraw_requests a JOIN member_accounts b WHERE a.status='Open' AND a.personID = b.personID")
        row = c.fetchone()
        allReqs = []
        while row is not None:
            closeup = "<button type='button' onclick='closeReq(\"" + row[4] + "\")'>Fulfill</button>"
            currReq = dict(game=row[3], date=row[2], key=row[4], amt=row[1], status=row[5], requestuser=row[6], closeup=closeup)
            allReqs.append(currReq)
            row = c.fetchone()
        c.close()
        conn.close()
        return allReqs
    else:
        return []

def getInfoOnKey(key, user, t):
    if isAdmin(user):
        c, conn = connection()
        if t == 'd':
            x = c.execute("SELECT a.*, b.* FROM deposit_requests a JOIN member_accounts b WHERE a.request_key = %s AND a.personID = b.personID",
                [escaper(key)])
        else:
            x = c.execute("SELECT a.*, b.* FROM withdraw_requests a JOIN member_accounts b WHERE a.request_key = %s AND a.personID = b.personID",
                [escaper(key)])
        if int(x) == 0:
            return []
        row = c.fetchone()
        return [row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[12]]
    else:
        return []

def makeDeposit(depkey, depuser, amt, type, user, rsname):
    if isAdmin(user) == True:
        c, conn = connection()
        c.execute("UPDATE deposit_requests SET status='Closed' WHERE request_key = %s", [escaper(depkey)])
        userid = getUserId(depuser)
        cashierid = getUserId(user)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO fulfilled_deposits (personID, cashierID, rsacc, amount, game_type, date_time, request_key) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                  [int(userid), int(cashierid), escaper(rsname), escaper(amt), escaper(type), escaper(st), escaper(depkey)])
        c.execute("UPDATE member_accounts SET balance = balance + %s WHERE username = %s", [int(amt), escaper(depuser)])
        conn.commit()
        c.close()
        conn.close()
    return

def makeWithdrawl(depkey, depuser, amt, type, user, rsname):
    if isAdmin(user) == True:
        c, conn = connection()
        c.execute("UPDATE withdraw_requests SET status='Closed' WHERE request_key = %s", [escaper(depkey)])
        userid = getUserId(depuser)
        cashierid = getUserId(user)
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO fulfilled_withdrawls (personID, cashierID, rsacc, amount, game_type, date_time, request_key) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                  [int(userid), int(cashierid), escaper(rsname), escaper(amt), escaper(type), escaper(st), escaper(depkey)])
        c.execute("UPDATE member_accounts SET balance = balance - %s WHERE username = %s", [int(amt), escaper(depuser)])
        conn.commit()
        c.close()
        conn.close()
    return

def checkBalance(user, amt):
    balance = getBalance(user)
    if balance >= int(amt):
        return True
    return False

def insertBet(user, amt, roll, res):
    userid = getUserId(user)
    c, conn = connection()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO fulfilled_bets (personID, amount, date_time, roll, result) VALUES (%s, %s, %s, %s, %s)", [int(userid), escaper(amt), escaper(st), escaper(roll), escaper(res)])
    if res == "W":
        c.execute("UPDATE member_accounts SET balance = balance + %s WHERE personID = %s", [int(escaper(amt)), int(userid)])
    else:
        c.execute("UPDATE member_accounts SET balance = balance - %s WHERE personID = %s",
                  [int(escaper(amt)), int(userid)])
    conn.commit()
    conn.close()
    return getBalance(user)
