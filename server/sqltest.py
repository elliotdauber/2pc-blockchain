import sqlite3


# might need this to import: https://stackoverflow.com/questions/19530974/how-can-i-add-the-sqlite3-module-to-python
def do():
    con = sqlite3.connect('db0.db')
    cursor = con.cursor()
    # Create table
    cursor.execute('''CREATE TABLE stocks
                   (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    cursor.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()


do()
