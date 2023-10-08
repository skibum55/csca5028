import sqlite3
import os
# Create a database with the filename given.
# Create the required tables and fields.

db_filename = os.environ.get("SQLITE_DB")

def create(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    # c = cur.execute("CREATE TABLE Store(idStore INTEGER PRIMARY KEY ASC, SquareFeet INTEGER,StoreType VARCHAR(45),LocationType CHAR(1), Address VARCHAR(45), City VARCHAR(45), StoreState VARCHAR(45), ZipCode VARCHAR(10) );")
    c = cur.execute("CREATE TABLE  IF NOT EXISTS Message(type string,text string,ts string);")
    conn.commit()
    conn.close()

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
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    # c = cur.executemany("INSERT INTO Store VALUES(?, ?, ?,?,?,?,?,?)", storeData) 
    c = cur.executemany("INSERT INTO Message VALUES(?,?,?,?)", messageData)
    conn.commit()
    conn.close 

# https://www.sqlitetutorial.net/sqlite-python/insert/
def insert(message):
    # db_filename="mydb"
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    c = cur.execute("INSERT INTO Message VALUES(?, ?,?)", message) 
    conn.commit()
    conn.close 

def select(message):
    # db_filename="mydb"
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    c = cur.execute("SELECT * FROM Message") 
    conn.commit()
    conn.close 