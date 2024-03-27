# app.py

from flask import Flask, render_template, request, redirect, session, url_for, send_file
import auth  # Import the Blueprint from auth.py
from flask_session import Session
import logging,models

# Configure the logger
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger('my_logger')

app = Flask(__name__)

Session(app)

app = Flask(__name__, static_folder='static')

# Register the Blueprint with the main app
myAuth = auth.AuthBlueprint('auth', __name__)
app.register_blueprint(myAuth)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the extension
Session(app)

@app.route('/', methods=['GET'])
def index():
    session['adminUpdates'] = "Hello World! Nice to meet you.\nThis is my starting point for creating my RNA."
    return render_template('base_application.html')

@app.route('/viewLogs/<category>', methods=['GET'])
def viewLogs (category):
    filteredLogs = []
    with open('app.log', 'r') as logFile:
        logs = logFile.readlines()
        for logEntry in logs:
            if 'logged in' in logEntry or 'logged out' in logEntry:
                filteredLogs.append(logEntry)
    return render_template('adminLogs.html', logs=filteredLogs, user=category)

@app.route('/clearLogs', methods = ['GET'])
def clearLogs ():
    logFilePath = 'app.log'
    with open(logFilePath, 'w'):
        pass
    
    return render_template('adminHome.html')

@app.route('/bookTicket/<category>/<id>', methods = ["GET","POST"])
def bookTicket (category,id):
    if request.method == "POST":
        myHelper = models.OtherRequiredTools()
        myEmail = request.form['myEmail']
        myNumber = request.form['myNumber']
        fromLoc = request.form['fromLoc']
        toLoc = request.form['toLoc']
        passengers = request.form['passengers']
        travelDate = request.form['travelDate']
        trainNumber = request.form['trainNumber']
        coach = request.form['coach']
        result = myHelper.bookingPhase1(id,myEmail,myNumber,fromLoc,toLoc,passengers,travelDate,trainNumber,coach)
        error = None
        if result[0] is True:
            return render_template('bookings2.html',user=category,id=id,count=int(passengers),coach=coach,bid=result[1])
        elif result[0] == 2:
            error = f"The date should be after today ({myHelper.sendTime()[0]})"
        elif type(result[0]) == type("Hello"):
            error = f"Expected train number should have 5 numbers (you gave {result} numbers)"
        return render_template('bookings.html',myEmail=myEmail,myNumber=myNumber,fromLoc=fromLoc
            ,toLoc=toLoc,passengers=passengers,travelDate=travelDate,trainNumber=trainNumber,error=error,user=category,id=id)
    return render_template('bookings.html', user=category, id=id)

@app.route('/finalizeBooking/<category>/<bid>/<id>/<count>/<coach>', methods = ["GET","POST"])
def finalizeBooking (category, bid, id, count, coach):
    if request.method == "POST":
        myHelper = models.OtherRequiredTools()
        cnt = int(count)
        names = []
        ages = []
        genders = []
        berths = []
        for i in range(cnt):
            names.append(request.form['name' + str(i+1)])
            ages.append(int(request.form['age' + str(i+1)]))
            genders.append(request.form['gender' + str(i+1)])
            berths.append(request.form['berth' + str(i+1)])

        result = myHelper.bookingPhase2(bid,id,names,ages,genders,berths,coach)

        if result[0] is True:
            return render_template("bookingSuccess.html",user=category,fileName=result[1])
        return render_template("bookings2.html", user=category, id=id, bid=bid, count=count, coach=coach)

@app.route('/openPDF/<fileName>', methods=['GET'])
def openPDF(fileName):
    return send_file(fileName,as_attachment=False)

@app.route('/giveAnnouncements/<category>', methods=['GET'])
def giveAnnouncements(category):
    return render_template('getDetails.html', category=category)

@app.route('/createAudio/<id>', methods = ['GET','POST'])
def createAudio(id):
    hours = request.form['hours']
    minutes = request.form['minutes']
    platNo = request.form['platNo']
    trainNo = request.form['trainNo']
    trainName = request.form['trainName']
    fromStation = request.form['fromStation']
    toStation = request.form['toStation']
    annType = request.form['annType']

    from gtts import gTTS
    import pygame,os

    temp_audio_file = "temp_audio.mp3"

    myList = list(trainNo)
    myList = ["zero" if (i == '0') else i for i in myList]
    formattedSentence = ""
    formattedSentence2 = ""

    if annType == "arrival":
        formattedSentence = "will arrive on"
        formattedSentence2 = f" at {hours} hours {minutes} minutes"
    elif annType == "depature":
        formattedSentence = "will depart from"
        formattedSentence2 = f" at {hours} hours {minutes} minutes"
    elif annType == "arrival shortly":
        formattedSentence = "will arrive shortly on"
    elif annType == "departure shortly":
        formattedSentence = "will depart shortly from"
    else:
        formattedSentence = "is at"

    text = f"Attention passengers. Train Number {' '.join(myList)}, the {trainName} traveling from {fromStation} to {toStation}, {formattedSentence} Platform number {platNo}{formattedSentence2}. Have a pleasant journey!"

    tts = gTTS(text)
    tts.save(temp_audio_file)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    
    #os.remove("temp_audio.mp3")
    return render_template('getDetails.html',category=id)

@app.route("/getBookings/<category>/<id>", methods = ['GET'])
def getBookings(category,id):
    myHelper = models.OtherRequiredTools()
    phase1 = myHelper.listOfPhaseOneBookings(id)
    phase2 = list()
    t = 0
    for i in phase1:
        phase2.append(myHelper.listOfPhaseTwoBookings(i[0])) #i[0] contains 2D array
        t += 1
    return render_template('myBookings.html', category = category, id = id, phase1 = phase1, phase2 = phase2)

@app.route("/cancelBooking/<category>/<id>/<bookId>", methods = ['GET'])
def cancelBooking(category, id, bookId):
    myHelper = models.OtherRequiredTools()
    myHelper.cancelIt(id,bookId)
    return redirect(f"/getBookings/{category}/{id}")

@app.route("/deletePastBookings/<category>", methods = ['GET'])
def deletePastBookings(category):
    myHelper = models.OtherRequiredTools()
    myHelper.deleteAll()
    return redirect(url_for('auth.loginForm', myCategory = category))

@app.route("/getRailSchedule/<category>", methods = ['GET'])
def getRailSchedule(category):
    return render_template('railSchedulesAPI.html', user=category)
if __name__ == '__main__':
    app.run(debug=True)
