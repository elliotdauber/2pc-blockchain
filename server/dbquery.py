import sqlite3
import sys

def query_pk(dbfile, table, pk):
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    _pk = None
    for row in cursor.execute("SELECT * FROM " + table + ";"):
        if row[0] == pk:
            _pk = row
    db.commit()
    db.close()
    return _pk

def query(dbfile, table):
    db = sqlite3.connect(dbfile)
    cursor = db.cursor()
    for row in cursor.execute("SELECT * FROM " + table + ";"):
        print(row)
    db.commit()
    db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("must have dbfile and table name")
    else:
        dbfile = sys.argv[1]
        table = sys.argv[2]
        query(dbfile, table)
