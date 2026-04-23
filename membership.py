from db import get_connection
from datetime import datetime, timedelta


def add_membership(name, email, duration):
    conn = get_connection()
    cursor = conn.cursor()

    # convert duration → months
    if duration == "6 months":
        months = 6
    elif duration == "1 year":
        months = 12
    else:
        months = 24

    # calculate end date
    end_date = datetime.now() + timedelta(days=30 * months)

    # insert data
    cursor.execute("""
        INSERT INTO Membership (Name, Email, Duration, EndDate)
        VALUES (?, ?, ?, ?)
    """, (name, email, duration, end_date))

    conn.commit()

    # get inserted ID
    mid = cursor.lastrowid

    conn.close()
    return mid


def get_member(mid):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Membership WHERE MembershipID=?", (mid,))
    data = cursor.fetchone()

    conn.close()
    return data


def extend_membership(mid):
    conn = get_connection()
    cursor = conn.cursor()

    # fetch current end date
    cursor.execute("SELECT EndDate FROM Membership WHERE MembershipID=?", (mid,))
    result = cursor.fetchone()

    if result and result[0]:
        current_end = datetime.fromisoformat(result[0])
    else:
        current_end = datetime.now()

    new_end = current_end + timedelta(days=180)  # +6 months

    cursor.execute("""
        UPDATE Membership
        SET EndDate=?
        WHERE MembershipID=?
    """, (new_end, mid))

    conn.commit()
    conn.close()


def cancel_membership(mid):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Membership
        SET Status='Cancelled'
        WHERE MembershipID=?
    """, (mid,))

    conn.commit()
    conn.close()