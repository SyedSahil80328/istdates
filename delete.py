import sqlite3
connect = sqlite3.connect('users.db')
cursor = connect.cursor()

try:
    cursor.execute("DELETE FROM USERS WHERE CATEGORY != 'Admin';")
    cursor.execute("DROP TABLE BOOKING_PHASE1;")
    cursor.execute("DROP TABLE BOOKING_PHASE2;")
    connect.commit()
except sqlite3.Error as e:
    print("Error in deletion")
    print (e)
finally:
    cursor.close()
    connect.close()
    print("Database closed successfully.")