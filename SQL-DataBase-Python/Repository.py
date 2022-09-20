import atexit
import sqlite3
import sys

from Hat import _Hats
from Order import _Orders
from Supplier import _Suppliers


class _Repository:
    hats = None
    orders = None
    suppliers = None
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(sys.argv[4])
        self.orders = _Orders(self.conn)
        self.suppliers = _Suppliers(self.conn)
        self.hats = _Hats(self.conn)

    def close(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.conn.executescript("""
        CREATE TABLE suppliers (id INT PRIMARY KEY, name STRING NOT NULL);
        
        CREATE TABLE hats (
        id          INT         PRIMARY KEY, 
        topping     STRING      NOT NULL, 
        supplier    INT         NOT NULL,
        quantity    INTEGER     NOT NULL,
        FOREIGN KEY(supplier) REFERENCES suppliers(id));
        
        CREATE TABLE orders (
        id       INTEGER    PRIMARY KEY,
        location STRING     NOT NULL,
        hat      INTEGER    NOT NULL, 
        FOREIGN KEY(hat) REFERENCES hats(id));
        """)




repo = _Repository()
atexit.register(repo.close)
