import sqlite3 
import functools

def with_db_connection(func):
    """ Decorator that manages the database connection """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        db_conn = sqlite3.connect('users.db') # open connection
        try:
            # injecting the connection as the first argument
            return func(db_conn, *args, **kwargs)
        finally:
            db_conn.close() # close connection
    return wrapper 

@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)