import MySQLdb
from MySQLdb import escape_string as escaper
import hashlib, uuid

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
