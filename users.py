"""
@author: steve
Updated by : Shashank Salunkhe
"""

import sqlite3
import uuid
import bottle
import database,interface

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

db=sqlite3.connect(database.DATABASE_NAME)


def check_login(db, usernick, password):
    """returns True if password matches stored"""
    db_password = get_password_by_nick(usernick)
    hash_password = database.password_hash(password)
    return True if (db_password == hash_password) else False


def get_password_by_nick(usernick):
    """Fetch user password by querying unique nick to the user table from database"""
    cursor = db.cursor()
    sql = "SELECT password FROM users WHERE nick = ?"
    cursor.execute(sql,(usernick,))
    row = cursor.fetchone()
    return None if row is None else row[0]


def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    if interface.check_user_valid(db,usernick):
        active_session = check_active_session(db,usernick)
        if active_session is None:
            key = str(uuid.uuid4())
            cursor = db.cursor()
            sql = "INSERT OR IGNORE INTO sessions (SESSIONID,USERNICK) VALUES (?,?)"
            cursor.execute(sql, (key, usernick,))
            db.commit()
        else:
            key = active_session[0]
        bottle.response.set_cookie(COOKIE_NAME,key)
        return key
    else:
        return None


def check_active_session(db,usernick):
    cursor = db.cursor()
    sql = "SELECT sessionid FROM sessions WHERE usernick = ?"
    cursor.execute(sql, (usernick,))
    return cursor.fetchone()

def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cursor = db.cursor()
    sql = "DELETE FROM sessions WHERE usernick = ?"
    cursor.execute(sql,(usernick,))
    db.commit()

def get_user_by_sessionid(db,sessionid):
    """Method to fetch username using the session id from sessions table"""
    cursor = db.cursor()
    sql = "SELECT usernick FROM sessions WHERE sessionid = ?"
    cursor.execute(sql,(sessionid,))
    row = cursor.fetchone()
    return None if row is None else row[0]


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    key = bottle.request.get_cookie(COOKIE_NAME)
    if key is None:
        return None
    else:
        return get_user_by_sessionid(db,key)

