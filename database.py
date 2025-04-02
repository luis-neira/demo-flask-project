from flask import g
import sqlite3


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


def get_db():
    """ Get a database connection that lasts for the request. """

    if "db" not in g:
        db = Database()
        db.connect("real-estate.db")
        g.db = db

    return g.db


def close_db(e=None):
    """ Close the database connection at the end of the request. """

    db = g.pop("db", None)

    if db:
        db.close()
