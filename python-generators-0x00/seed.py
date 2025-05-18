import mysql.connector
import csv
import uuid

def connect_db():
    """Function to connect to mysql database server"""
    try:
        connection_db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kmoney007'
        )
        if connection_db.is_connected():
            print("Successfully connected to mySQL server")
            return connection_db
    except mysql.connector.Error as err:
        print(f"failed to connect to mysql: {err}") 
        return None

def create_database(connection):
    """Create database for ALX_prodev 
    if it doesnt exist
    """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()        

def connect_to_prodev():
    """connects the the ALX_prodev database in MYSQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kmoney007',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """creates a table user_data if it does not
    exists with the required fields
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3, 0) NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("user_data table created")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")



def insert_data(connection, data):
    """inserts data in the database if it does not exist"""
    try:
        cursor = connection.cursor()
        for row in data:
            user_id = str(uuid.uuid4())
            name, email, age = row['name'], row['email'], row['age']

            # Check if email already exist
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")

def read_csv_data(file_path):
    """Reads the CSV file and return
    a list of dictionaries"""
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
            print(f"Loaded {len(data)} rows from {file_path}")
            return data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def main():
    # Connect mysql server
    db_connection = connect_db()
    if db_connection:
        # create the database
        create_database(db_connection)
        db_connection.close()

    # connect to ALX_prodev database
    db_connection = connect_to_prodev()
    if db_connection:
        # create the user table
        create_table(db_connection)
        user_data = read_csv_data('user_data.csv')
        # insert data
        insert_data(db_connection, user_data)
        db_connection.close()

if __name__ == "__main__":
    main()                