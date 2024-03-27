# models.py

import sqlite3, traceback, datetime, random, pdfkit, os
from flask import session
import TDES

class OtherRequiredTools:
    def __init__ (self):
        self.connection = None  #For connecting with database
        self.cursor = None      #For creating a cursor to use DML commands
        self.fetchedList = []   #Storing a list of items
        self.myList = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"*7
        self.myList2 = "0123456789"*35
                                #For generating a random user ID
        self.currTime = ""
        self.currDate = ""
        self.currTimeStamp = None   #Variables for time extraction

    def createUser(self, username, email, password, category = "Customer"):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        safePassword = TDES.enpsd(password)

        try:
            self.cursor.execute("SELECT EMAIL FROM USERS WHERE CATEGORY = ?;", (category,))
            self.fetchedList = self.cursor.fetchall()
            if (email,) not in self.fetchedList: #Checks if the given email already exists
                self.cursor.execute("SELECT ID FROM USERS WHERE CATEGORY = ?;", (category,))
                myId = self.randId()
                self.fetchedList = self.cursor.fetchall()         
                while (1):
                    if (myId,) not in self.fetchedList: #Checks if the generated ID already exists
                        self.cursor.execute("INSERT INTO USERS VALUES (?, ?, ?, ?, ?);", (myId, username, email, safePassword, category))
                        self.connection.commit()
                        return True
                    myId = self.randId() #If already exists, it'll continuously executed to get unique ID
            return email + "2"  #Return statement for email already existing
        
        except Exception as e:
            self.connection.rollback()
            traceback.print_exc()
            return str(e)
        finally:
            self.connection.close()

    def validateUser (self, email, password, category):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(f"SELECT NAME, PASSWORD, ID FROM USERS WHERE EMAIL = '{email}' AND CATEGORY = '{category}';")
            List = self.cursor.fetchall()
            if len(List) == 0:  #If a user with email is not found
                return "not exist"
            
            print(List[0][1], TDES.enpsd(password))
            if List[0][1] == TDES.enpsd(password):  #If the entered password is equal to stored password
                return [List[0][0],List[0][2],email] #Sends Username, ID and email 
            return False    #Implies password is invalid
        except sqlite3.Error as e:
            self.connection.rollback()
            return str(e)
        finally:
            self.connection.close()

    def sendTime (self):
        self.currTimeStamp = datetime.datetime.now()
        self.currDate = self.currTimeStamp.strftime("%d/%m/%Y") 
        self.currTime = self.currTimeStamp.strftime("%I:%M:%S %p")
        return [self.currDate, self.currTime]

    def updatePassword (self, mySession, existing, new, confirm, category):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"SELECT PASSWORD FROM USERS WHERE CATEGORY = '{category}' AND ID = '{session[mySession][1]}' AND EMAIL = '{session[mySession][2]}';")
        self.fetchedList = self.cursor.fetchall()   

        if self.fetchedList[0][0] != TDES.enpsd(existing):
            return "Invalid Password"
        if new != confirm:
            return "Not matching"
    
        self.cursor.execute(f"UPDATE USERS SET PASSWORD = '{TDES.enpsd(new)}' WHERE CATEGORY = '{category}' AND ID = '{session[mySession][1]}' AND EMAIL = '{session[mySession][2]}';")
        self.connection.commit()
        self.connection.close()
        return True
    
    def randId(self,randId = "General"):
        if randId == "General":
            return "".join(random.sample(self.myList, 20))
        return "".join(random.sample(self.myList2, 20))
    
    def bookingPhase1(self,id,myEmail,myNumber,fromLoc,toLoc,passengers,travelDate,trainNumber,coach):
        today = datetime.datetime.now().date()
        myDate = datetime.datetime.strptime(travelDate,"%Y-%m-%d").date()

        if today > myDate:
            return [2]
        if len(str(trainNumber)) != 5:
            return [str(len(str(trainNumber)))]
        
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

        myID = self.randId()
        inserted = False
        self.cursor.execute(f"""INSERT INTO BOOKING_PHASE1 VALUES ('{myID}','{id}','{myEmail}',
        {myNumber},'{fromLoc}','{toLoc}',{passengers},'{travelDate}',{trainNumber},'{coach}');""")
        self.connection.commit()
        self.connection.close()
        return [True,myID]
    
    def bookingPhase2(self,bookID,id,names,ages,genders,berths,coach):
        rate = 0
        if coach == "First Class AC":
            rate = random.randint(2000,3000)
        elif coach == "AC 2 Tier":
            rate = random.randint(1820,2070)
        elif coach == "AC 3 Tier":
            rate = random.randint(1520,1845)
        elif coach == "AC Chair Car":
            rate = random.randint(820,1245)
        elif coach == "Sleeper Non-AC":
            rate = random.randint(820,1587)
        elif coach == "Second Class":
            rate = random.randint(425,887)
        elif coach == "Chair Car":
            rate = random.randint(432,919)
        else:
            rate = random.randint(223,540)

        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        amounts = []
        intAmounts = []
        
        for i in range(len(names)):
            myId = self.randId("Passenger")
            if ages[i] >= 0 and ages[i] <= 5:
                amount = 0
            elif ages[i] <= 12:
                amount = rate/2
            elif ages[i] <= 60:
                amount = rate
            else:
                amount = rate * 0.6
            try:
                self.cursor.execute(f"""INSERT INTO BOOKING_PHASE2 VALUES 
                ('{myId}','{bookID}','{names[i]}',{ages[i]},'{genders[i]}','{berths[i]}',{amount});""")
                amounts.append("₹ " + str(amount))
                intAmounts.append(amount)
            except Exception as e:
                i -= 1
        
        self.connection.commit()
        self.cursor.execute(f"SELECT * FROM BOOKING_PHASE1 WHERE BOOKING_ID = '{bookID}' AND ID = '{id}';")
        r = self.cursor.fetchall()
        myFile = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Railway Ticket</title>
</head>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f0f0f0;
        text-align: center;
    }}

    .ticket {{
        max-width: 1000px;
        margin: 20px auto;
        background-color: white;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}

    .ticket-header {{
        text-align: center;
    }}

    .ticket-header h1 {{
        font-size: 24px;
        margin: 0;
        color: #333;
    }}

    .ticket-info table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .ticket-info th, .ticket-info td {{
        padding: 8px;
        border-bottom: 1px solid #ddd;
        text-align: center;
    }}

    .ticket-info th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}

    .passenger-details {{
        margin-top: 20px;
    }}

    .passenger-details h2 {{
        font-size: 20px;
        margin: 0;
        color: #333;
    }}

    .passenger-details table {{
        width: 100%;
        border-collapse: collapse;
    }}

    .passenger-details th, .passenger-details td {{
        padding: 8px;
        border-bottom: 1px solid #ddd;
        text-align: center;
    }}

    .passenger-details th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}

    .total-fare p {{
        margin-top: 20px;
        font-weight: bold;
        font-size: 18px;
    }}

    .header {{
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }}

    .icon {{
        width: 40px;
        height: 40px;
        margin-right: 10px;
    }}

    .footer {{
        margin-top: 20px;
        font-size: 14px;
        color: #888;
        text-align: center;
    }}

    .assistance-tips {{
        font-style: italic;
    }}
</style>
<body>
    <div class="ticket">
        <div class="ticket-header">
            <h1>Railway Ticket</h1>
            <p>Email ID: {r[0][2]}</p>
            <p>Train Number: {r[0][8]}</p>
        </div>
        <div class="ticket-info">
            <table>
                <tr>
                    <th>From</th>
                    <th>To</th>
                    <th>Phone Number</th>
                    <th>Passengers</th>
                    <th>Date of Boarding</th>
                    <th>Preferred Coach</th>
                </tr>
                <tr>
                    <td>{r[0][4]}</td>
                    <td>{r[0][5]}</td>
                    <td>{r[0][3]}</td>
                    <td>{r[0][6]}</td>
                    <td>{r[0][7]}</td>
                    <td>{r[0][9]}</td>
                </tr>
            </table>
        </div>
        <div class="passenger-details">
            <h2>Passenger Details</h2>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Gender</th>
                    <th>Berth Preference</th>
                    <th>Rate</th>
                </tr>
                <tbody id="passengerDetails"></tbody>
            </table>
        </div>
        <div class="total-fare">
            <p>Total Fare: ₹{sum(intAmounts)}</p>
        </div>
        <div class="footer">
            <p>© 2023 Railway Department. All rights reserved.</p>
            <p class="assistance-tips">For assistance, call 1234567890 or email support@railways.com</p>
        </div>
    </div>
</body>
<script>
    e = document.getElementById('passengerDetails');
    keys = ['name','age','gender','preference','rate'];
    details = {{
        name: {names},
        age: {ages},
        gender: {genders},
        preference: {berths},
        rate: {amounts}
    }};
    for (i=0 ; i<{len(names)} ; i++) {{
        myRow = document.createElement('tr');
        for (j=0 ; j<5 ; j++) {{
            myDeck = document.createElement('td');
            myDeck.textContent = details[keys[j]][i];
            myRow.appendChild(myDeck);
        }}
        e.appendChild(myRow);
    }}
</script>
</html>

"""
        options = {
    'page-size': 'Letter',
    'orientation': 'Landscape',  # Set orientation to Landscape
    'no-images': None  # If you want to include images, remove this line
}
        pdfkit.from_string(myFile, id + "_" + bookID +'.pdf',options=options)
        self.connection.close()
        return [True,id + "_" + bookID +'.pdf']

    def listOfPhaseOneBookings(self, myId):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"SELECT * FROM BOOKING_PHASE1 WHERE ID = '{myId}';")

        e = self.cursor.fetchall()
        j = 0
        for i in e:
            e[j] = list(i)
            j += 1
        
        self.connection.close()
        return e
    
    def listOfPhaseTwoBookings(self, myBookingId):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"SELECT * FROM BOOKING_PHASE2 WHERE BOOKING_ID = '{myBookingId}';")

        e = self.cursor.fetchall()
        j = 0
        for i in e:
            e[j] = list(i)
            j += 1
        
        self.connection.close()
        return e
    
    def cancelIt(self, id, bookId):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        os.remove(f"{id}_{bookId}.pdf")

        self.cursor.execute(f"DELETE FROM BOOKING_PHASE2 WHERE BOOKING_ID = '{bookId}';")
        self.cursor.execute(f"DELETE FROM BOOKING_PHASE1 WHERE ID = '{id}' AND BOOKING_ID = '{bookId}';")

        self.connection.commit()
        self.connection.close()
    
    def deleteAll(self):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()
        myDate = datetime.datetime.now().date()
        print("Operation for deleting all old bookings.")
        self.cursor.execute(f"""SELECT ID, BOOKING_ID FROM BOOKING_PHASE1 WHERE TRAVELDATE < '{myDate}';""")
        e = self.cursor.fetchall()
        if len(e) == 0:
            print("Result: No fields detected.")
        else:
            for i in e:
                self.cursor.execute(f"""DELETE FROM BOOKING_PHASE2 WHERE BOOKING_ID = '{i[1]}';""")
                os.remove(f"{i[0]}_{i[1]}.pdf")
            self.cursor.execute(f"""DELETE FROM BOOKING_PHASE1 WHERE TRAVELDATE = '{myDate}';""")
            self.connection.commit()
            print(f"Result: Found {len(e)} bookings. Deleted Successfully.")
        self.connection.close()