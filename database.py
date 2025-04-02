from flask import g
import sqlite3


def get_db():
    """Get a database connection that lasts for the request."""

    if "db" not in g:
        conn = sqlite3.connect("real-estate.db")
        g.db = {
            "conn": conn,
            "cursor": conn.cursor()
        }
        # g.db.row_factory = sqlite3.Row  # Enables dict-like row access
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""

    db = g.pop("db", None)

    if db is not None:
        db.get("cursor").close()
        db.get("conn").close()
