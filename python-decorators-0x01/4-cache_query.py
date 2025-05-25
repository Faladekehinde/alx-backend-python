import time
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    """decorator that caches the results of a database
    queries inorder to avoid redundant calls
    """
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("returning cached result for query", query)
            return query_cache[query]
        print("Executing queries and caching results", query)
        result = func(conn, query)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")