from db import get_connection

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Role FROM Users WHERE Username=? AND Password=?",
        (username, password)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # admin / user
    return None