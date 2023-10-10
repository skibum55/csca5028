import sqlite3
import os
from contextlib import contextmanager
# createdb & session
db_path = os.environ.get("SQLITE_DB")

@contextmanager
def db_cursor(db_path):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        yield cur
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close() 

# Create a database with the filename given.
# Create the required tables and fields

def create(db_filename):
    # conn = sqlite3.connect(db_filename)
    with db_cursor(db_path) as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS messageSentiment(ts string, sentiment string);")
        cur.execute("CREATE TABLE IF NOT EXISTS message(type string,text string,ts string);")


storeData = [
    (1, 1982, 'Big','R','right down the street','acity','ca','12345'),
    (2, 1983, 'medium','G','right across the street','bcity','co','54321'),
    (3, 1984, 'small','B','near the street','ccity','ak','56789'),
]

messageData = [
    ('message', "For the final project, I see there 3 levels(A, B and C) in the project rubric. Does that mean I can’t get a full score(100%) if it only meets C level work requirements?", '1403051575.000407'),
    ('message',"could anyone review my Week 5 assignment please?", '1403051575.000408'),
    ('message',"I've got some API credentials which I'm not putting in my public repository.  Do y'all think adding those in my Project submission notes is a good way to share them with the peer reviewer?", '1403051575.000409'),
]

def fill(db_filename):
    with db_cursor(db_path) as cur:
        # c = cur.executemany("INSERT INTO Store VALUES(?, ?, ?,?,?,?,?,?)", storeData) 
        cur.executemany("INSERT INTO Message VALUES(?,?,?,?)", messageData)

# https://www.sqlitetutorial.net/sqlite-python/insert/
def insert(message):
    # db_filename="mydb"
    # conn = sqlite3.connect(db_filename)
    with db_cursor(db_path) as cur:
        cur.execute("INSERT INTO Message VALUES(?, ?,?)", message) 
 

def select(message):
    with db_cursor(db_path) as cur:    
        cur.execute("SELECT * FROM Message") 
