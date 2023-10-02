import sqlite3
# Create a database with the filename given.
# Create the required tables and fields.
#
def create(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    c = cur.execute("CREATE TABLE Store(idStore INTEGER PRIMARY KEY ASC, SquareFeet INTEGER,StoreType VARCHAR(45),LocationType CHAR(1), Address VARCHAR(45), City VARCHAR(45), StoreState VARCHAR(45), ZipCode VARCHAR(10) );")
    c = cur.execute("CREATE TABLE Product(idProduct INTEGER, Name VARCHAR(30), Price DECIMAL, CategoryID INTEGER, Description VARCHAR(90), PRIMARY KEY(idProduct));")
    c = cur.execute("CREATE TABLE Store_Product(ProductID INTEGER, StoreID INTEGER, Quantity INTEGER, PRIMARY KEY(ProductID,StoreID));")
    c = cur.execute("CREATE TABLE Category(idCategory INTEGER PRIMARY KEY ASC, Name VARCHAR(45), Description VARCHAR(90));")
    conn.commit()
    conn.close()

storeData = [
    (1, 1982, 'Big','R','right down the street','acity','ca','12345'),
    (2, 1983, 'medium','G','right across the street','bcity','co','54321'),
    (3, 1984, 'small','B','near the street','ccity','ak','56789'),
]

productData = [
    (1,"product1",3.33,1,"the best product"),
    (2,"product2",2.22,2,"a good product"),
    (3,"product3",1.11,3,"the real product"),
    # select idCategory from Category c where c.name="category2
]

categoryData = [                                              
    (1, 'category1', 'the first category'),
    (2, 'category2', 'the second category'),
    (3, 'category3', 'the final category'),                  
]

storeProductData = [                                           
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]

def fill(db_filename):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    c = cur.executemany("INSERT INTO Category VALUES(?, ?, ?)", categoryData)
    c = cur.executemany("INSERT INTO Store VALUES(?, ?, ?,?,?,?,?,?)", storeData) 
    c = cur.executemany("INSERT INTO Product VALUES(?, ?, ?,?,?)", productData) 
    c = cur.executemany("INSERT INTO Store_Product VALUES(?, ?, ?)", storeProductData) 
    conn.commit()
    conn.close 