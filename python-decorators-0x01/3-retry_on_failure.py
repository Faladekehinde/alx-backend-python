import time
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

def retry_on_failure(retries=3, delay=2):
    """ retries database operations if they fail due to transient errors"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **Kwargs)
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                    last_exception = e
                    time.sleep(delay)
            #when all retries fails, raise the last error
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)