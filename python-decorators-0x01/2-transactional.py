import sqlite3 
import functools

def with_db_connection(func):
    """ Decorator that manages the database connection """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db') # open connection
        try:
            # injecting the connection as the first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close() # close connection
    return wrapper

def transactional(func):
    """Decorator to manage database transaction"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            output = func(conn, *args, **kwargs) # if everything worked
            conn.commit() # save changes
            return output
        except Exception:
            conn.rollback() # if an error occured, undo chnages
            raise # raise the error
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')