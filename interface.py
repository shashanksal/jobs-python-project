"""
Database Model interface for the COMP249 Web Application assignment

Updated By : Shashank Salunkhe
"""

import sqlite3
import database,datetime

db= sqlite3.connect(database.DATABASE_NAME)


def position_list(db, limit=10):
    """Return a list of positions ordered by date
    db is a database connection
    return at most limit positions (default 10)

    Returns a list of tuples  (id, timestamp, owner, title, location, company, description)
    """
    cursor = db.cursor()
    sql = "SELECT * FROM positions ORDER BY date(timestamp) DESC Limit ?"
    cursor.execute(sql,(limit,))
    return list(cursor)



def position_get(db, id):
    """Return the details of the position with the given id
    or None if there is no position with this id

    Returns a tuple (id, timestamp, owner, title, location, company, description)

    """
    cursor = db.cursor()
    sql = "SELECT * FROM positions where id = ?"
    cursor.execute(sql, (id,))
    return (cursor.fetchone())

def get_users_nick(db):
    # Get list of user nick
    cursor = db.cursor()
    sql = "SELECT nick FROM users"
    cursor.execute(sql)
    k= (i[0] for i in list(cursor)) #extracting 1st element from list of tuple and returning them in a list
    return list(k)



def position_add(db, usernick, title, location, company, description):
    """Add a new post to the database.
    The date of the post will be the current time and date.
    Only add the record if usernick matches an existing user

    Return True if the record was added, False if not."""

    if check_user_valid(db,usernick): # Checking valid user and then and only then performing the operations
        cursor = db.cursor()
        sql = "INSERT OR IGNORE INTO positions (TIMESTAMP, OWNER , TITLE, LOCATION, COMPANY, DESCRIPTION) VALUES (?,?,?,?,?,?)"
        cursor.execute(sql,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),usernick,title,location,company,description,))
        db.commit()
        return True # Return true of position is added
    else:
        return False # Else return false


def check_user_valid(db,nick):
    # Method to check if the usernick matches any existing user
    # Returns boolean True if the user is existing or False if not.
    users = get_users_nick(db) #Fetching all user nick list
    try:
        index = users.index(nick) # Getting the index position of the matched nick from the list of nicks
        # If the matched nick exists, it returns a non negative value otherwise throws an exception
    except:
        index = -1 # Catching exception and assigning index as negative
    return True if (index != -1) else False # Terniary operator for returning result of matched valid user


