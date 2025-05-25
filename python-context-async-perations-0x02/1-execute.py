import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.ouputs = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.excute(self.query, self.params)
        self.outputs = cursor.fetchall()
        return self.outputs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as outputs:
    print(outputs)