import sqlite3
from flask import g

class DatabaseManager:
    def __init__(self, database_path):
        self.database_path = database_path
        self._init_db()

    def _init_db(self):
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
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.database_path)
        return db
