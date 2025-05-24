import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries
def log_queries():
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # get the current time
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Get query from args or kwargs
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else 'UNKNOWN QUERY'

        # log the query with timestamp
        print(f"{[timestamp]}Executing query: {'query'}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")