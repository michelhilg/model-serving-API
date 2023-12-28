import sqlite3
from flask import g

class DatabaseManager:
    """A Python class using sqlite3 for database related methods."""
    
    def __init__(self, database_path):
        """Initialize the DatabaseManager instance."""
        self.database_path = database_path
        self._init_db()

    def _init_db(self):
        """Initialize the database by creating a table if it doesn't exist."""
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identificadores (
                id INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()
        conn.close()

    def get_db(self):
        """
        Get the SQLite database connection.

        Returns:
        - sqlite3.Connection: SQLite database connection.
        """
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.database_path)
        return db
