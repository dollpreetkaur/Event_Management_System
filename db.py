import sqlite3

def get_connection():
    conn = sqlite3.connect("event.db", check_same_thread=False)
    return conn
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT,
        Password TEXT,
        Role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Membership (
        MembershipID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Email TEXT,
        Duration TEXT,
        StartDate TEXT DEFAULT CURRENT_TIMESTAMP,
        EndDate TEXT,
        Status TEXT DEFAULT 'Active'
    )
    """)

    # insert default users (only once)
    cursor.execute("SELECT * FROM Users")
    if not cursor.fetchall():
        cursor.execute("INSERT INTO Users VALUES (NULL,'admin','admin123','admin')")
        cursor.execute("INSERT INTO Users VALUES (NULL,'user1','user123','user')")

    conn.commit()
    conn.close()