import mysql.connector

def stream_users():
    """function that uses a generator to fetch rows
    one by one from the user_data table. You must use
    the Yield python generator
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kmoney007',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            # convert decimal Age into integer
            row['age'] = int(row['age'])
            yield row
        cursor.close()
        connection.close()
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")