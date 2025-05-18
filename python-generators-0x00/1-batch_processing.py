import mysql.connector
from decimal import Decimal

def stream_users_in_batches(batch_size):
    """fetches rows in batches"""
    db_connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pwd123',
        database='ALX_prodev'
    )
    cursor = db_connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()["COUNT(*)"]

    for offset in range(0, total, batch_size):
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
        )
        batch = cursor.fetchall()
        yield batch

    cursor.close()
    db_connection.close()

def batch_processing(batch_size):
    """processes each batch to filter users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            age = user['age']
            if isinstance(age, Decimal):
                age = int(age)
            if age > 25:
                print(user)
    return