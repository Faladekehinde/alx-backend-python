from seed import connect_to_prodev
from decimal import Decimal

def paginate_users(page_size, offset):
    """fetch the next page when needed at an offset of 0"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()

    for row in rows:
        if isinstance(row.get('age'), Decimal):
            row['age'] = int(row['age'])
    return rows

def lazy_pagination(page_size):
    """enerator to lazily load each page"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size