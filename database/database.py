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
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                feature_1 REAL,
                feature_2 REAL,
                prediction REAL
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
    
    def write(self, timestamp, feature_1, feature_2, prediction):
        """Writes the specify data into the database"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (timestamp, feature_1, feature_2, prediction)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, feature_1, feature_2, prediction))
            conn.commit()
            last_id = cursor.lastrowid 
            return last_id
