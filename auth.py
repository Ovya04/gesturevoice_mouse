import sqlite3
import hashlib

def connect():
    return sqlite3.connect("users.db")

def setup_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)
    con.commit()
    con.close()

def hash_pwd(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def register(username, password):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users VALUES (?,?)",
                    (username, hash_pwd(password)))
        con.commit()
        return True
    except:
        return False
    finally:
        con.close()

def login(username, password):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (username, hash_pwd(password)))
    result = cur.fetchone()
    con.close()
    return result is not None
