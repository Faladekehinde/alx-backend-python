import sqlite3

class DatabaseConnection:
    """ handle opening and closing database connections automatically"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # runs when we enter the 'with' block
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        # runs when we exit the 'with' block
        if self.conn:
            self.conn.close() # close the connection

# Using context manager to query the database
with DatabaseConnection("user.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    output = cursor.fetchall()
    print(output)