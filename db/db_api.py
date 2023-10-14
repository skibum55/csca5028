"""Function printing python version."""
import sqlite3
import os
from contextlib import contextmanager

# createdb & session
db_path = os.environ.get("SQLITE_DB") or "test.db"

# decorated for reuse - https://stackoverflow.com/questions/67436362/decorator-for-sqlite3/67436763#67436763
@contextmanager
def db_cursor(db_path):
    """Function printing python version."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
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
    """Function printing python version."""
    # https://www.linkedin.com/pulse/context-manager-python-asad-iqbal
    with db_cursor(db_path) as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS messageSentiment(ts string, sentiment string, confidence real);")
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

# TODO - make this into a mock ^^^
def fill(db_filename):
    """Function to create mock."""
    with db_cursor(db_path) as cur:
        # c = cur.executemany("INSERT INTO Store VALUES(?, ?, ?,?,?,?,?,?)", storeData) 
        cur.executemany("INSERT INTO message VALUES(?,?,?,?)", messageData)

# https://www.sqlitetutorial.net/sqlite-python/insert/
def insert(message):
    """Function to insert message."""
    # db_filename="mydb"
    # conn = sqlite3.connect(db_filename)
    with db_cursor(db_path) as cur:
        cur.execute("INSERT INTO message VALUES(?, ?,?)", message) 

def insert_sentiment(ts, sentiment, confidence):
    """Function to update sentiment table."""
    # db_filename="mydb"
    # conn = sqlite3.connect(db_filename)
    with db_cursor(db_path) as cur:
        cur.execute("INSERT INTO messageSentiment values (?,?,?)",(ts,sentiment,confidence))

def select(message):
    """function to select all messages"""
    with db_cursor(db_path) as cur:    
        cur.execute("SELECT * FROM message")

# https://stackoverflow.com/questions/50074564/python-sqlite3-selecting-rows-from-table
def get_latest():
    """function to get latest message in database"""
    with db_cursor(db_path) as cur:    
        for (timestamp,) in cur.execute("SELECT max(ts) as timestamp FROM message"): 
            return timestamp or 1

def get_average_sentiment():
    """Function printing python version."""
    with db_cursor(db_path) as cur:
        for (average,) in cur.execute("select avg(confidence) as average from messageSentiment"):
            return str(average)
        
def get_daily_sentiment(tag):
    """Function printing python version."""
    with db_cursor(db_path) as cur:
        # results = cur.execute("""SELECT json_group_array(json_object('sentiment',sentiment,'count', COUNT(sentiment), 'day', strftime('%Y-%m-%d',datetime(ts,'unixepoch')))) FROM messageSentiment ms GROUP BY day,sentiment;""")
        # results = cur.execute("""SELECT json_group_array(json_object('sentiment',sentiment,'day', strftime('%Y-%m-%d',datetime(ts,'unixepoch')))) FROM messageSentiment """)
        # results = cur.execute("""SELECT strftime('%Y-%m-%d',datetime(ts,'unixepoch')) as day, json_group_object(sentiment,confidence) as conf FROM messageSentiment group by day; """)
        # results = cur.execute("""SELECT strftime('%Y-%m-%d',datetime(ts,'unixepoch')) as day, json_array(sentiment,count(confidence)) FROM messageSentiment group by day; """)
        # results = cur.execute("""SELECT sentiment, json_group_array(strftime('%Y-%m-%d',datetime(ts,'unixepoch'))) ,count(confidence) FROM messageSentiment group by sentiment; """)
        rows = cur.execute("""SELECT strftime('%Y-%m-%d',datetime(ts,'unixepoch')) as day, COUNT(sentiment) as count
            FROM messageSentiment ms 
            where sentiment = '""" + tag + """'
            GROUP BY day;""").fetchall()
        # print(rows)
        rowarray_list = []
        for row in rows:
            d = dict(zip(row.keys(), row))   # a dict with column names as keys
            rowarray_list.append(d)
        # return rowarray_list
        return rows
