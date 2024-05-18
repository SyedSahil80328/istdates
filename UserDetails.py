import sqlite3
import pandas as pd
connect = sqlite3.connect('users.db')
cursor = connect.cursor()

try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS USERS (ID CHAR(20) PRIMARY KEY, NAME VARCHAR(50) NOT NULL, EMAIL VARCHAR(100) NOT NULL, PASSWORD VARCHAR(100) NOT NULL, CATEGORY VARCHAR(25) NOT NULL);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS BOOKING_PHASE1 (BOOKING_ID CHAR(20) PRIMARY KEY, ID CHAR(20) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL, PHONE BIGINT(10) NOT NULL, FROMSTOP VARCHAR(50) NOT NULL, 
    TOSTOP VARCHAR(50) NOT NULL, PASSENGERS INT NOT NULL, TRAVELDATE DATE NOT NULL, TRAINNO BIGINT(5) NOT NULL, PREFERENCES VARCHAR(30) NOT NULL);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS BOOKING_PHASE2 (PASSENGER_ID CHAR(20) PRIMARY KEY, BOOKING_ID CHAR(20) NOT NULL,
    NAME VARCHAR(50) NOT NULL, AGE INT NOT NULL, GENDER VARCHAR(6) NOT NULL, 
    BERTH VARCHAR(20) NOT NULL, RATE NUMERIC(9,3) NOT NULL);""")

    cursor.execute("""SELECT * FROM USERS;""")
    f = cursor.fetchall()
    userData = pd.DataFrame(f, columns=["User ID", "Name", "Email", "Password", "Category"])
    with pd.option_context('display.max_colwidth', None):
        print(userData.map(repr))

finally:
    cursor.close()
    connect.commit()
    connect.close()
