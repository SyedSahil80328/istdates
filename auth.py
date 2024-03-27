# auth.py

from flask import Blueprint, render_template, request, redirect, url_for, session, Response
import models
import logging

class AuthBlueprint(Blueprint):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        self.route('/signup', methods=['GET'])(self.signupForm)
        self.route('/signup', methods=['POST'])(self.signup)
        self.route('/signupSuccess/<username>', methods=['GET'])(self.signupSuccess)
        self.route('/login', methods=['GET'])(self.loginForm)
        self.route('/login', methods=['POST'])(self.login)
        self.route('/logout', methods=['GET'])(self.logout)
        self.route('/changePassword', methods=['GET'])(self.changePassword)
        self.route('/addUser', methods=['GET'])(self.addUser)
        self.route('/changeIt', methods=['GET', 'POST'])(self.changeIt)
        logging.basicConfig(filename='app.log', level=logging.INFO)
        self.logger = logging.getLogger('my_logger')

        self.otherRequiredTools = models.OtherRequiredTools() #Import functionalities of models.py
        self.username = ""          #Username for signup, login, railway booking, etc
        self.email = ""             #Email of user with same purpose as in Username
        self.password = ""          #Password for authentication
        self.npassword = ""
        self.cpassword = ""         #Both are used for confirmation and signup
        self.result = None          #Authentication results
        self.errorMessage = None    #Message variable to display errors
        self.myCategory = ""        #Categories include Passenger, Clerk, Master, Admin.
        self.mySession = ""         
        self.myTime = []            #Time at which user has logged in or logged out

    def signupForm(self):
        return render_template('signup.html')

    def signup(self):
        if request.method == 'POST':
            self.username = request.form['username']
            self.email = request.form['email']
            self.npassword = request.form['npassword']
            self.cpassword = request.form['cpassword']

            if self.npassword != self.cpassword:
                self.errorMessage = "Passwords do not match."
            else:
                try:
                    self.myCategory = request.form['category']
                    self.result = self.otherRequiredTools.createUser(self.username, self.email, self.npassword, self.myCategory)
                except Exception as e:
                    self.result = self.otherRequiredTools.createUser(self.username, self.email, self.npassword)
                finally:
                    if self.result is True:
                        return redirect(url_for('auth.signupSuccess', username=self.username))
                    else:
                        self.errorMessage = "Mail ID already exists."

            return render_template('signup.html', signupName=self.username, signupEmail=self.email, errorMessage=self.errorMessage)

        return render_template('signup.html')

    def signupSuccess(self, username):
        return render_template('signupSuccess.html')

    def loginForm(self):
        self.myCategory = request.args.get('myCategory')

        if self.myCategory.lower() + "Logged" in session:
            return render_template(self.myCategory.lower() + 'Home.html')

        response = Response(render_template('login.html', cat=self.myCategory))
        return response

    def login(self):
        self.myCategory = request.args.get('myCategory')

        if request.method == 'POST':
            self.email = request.form['email']
            self.password = request.form['password']
            self.result = self.otherRequiredTools.validateUser(self.email, self.password, self.myCategory)

            if self.result != "not exist" and self.result:
                self.myTime = self.otherRequiredTools.sendTime()
                self.mySession = self.myCategory.lower() + "Logged"
                session[self.mySession] = self.result
                self.logger.info('User {} logged in on {} at {}.'.format(self.result[0], self.myTime[0], self.myTime[1]))
                return render_template(self.myCategory.lower() + 'Home.html')

            if self.result == "not exist":
                self.errorMessage = "This email ID doesn't exist. Check for typos or create a new account."
            else:
                self.errorMessage = "Invalid password."
            return render_template('login.html', loginEmail=self.email, errorMessage=self.errorMessage, cat=self.myCategory)

    def logout(self):
        try:
            self.myCategory = request.args.get('cat')
            self.myTime = self.otherRequiredTools.sendTime()

            self.mySession = self.myCategory.lower() + "Logged"
            self.logger.info('User {} logged out on {} at {}.'.format(session[self.mySession][0], self.myTime[0], self.myTime[1]))
            session.pop(self.mySession, None)
            response = Response(render_template('logout.html', email=session))
            return response
        except Exception as e:
            return render_template('login.html', cat=self.myCategory)

    def changePassword(self):
        self.myCategory = request.args.get('logger')
        return render_template('changePassword.html', user=self.myCategory)

    def changeIt(self):
        self.myCategory = request.args.get('logger')
        self.mySession = self.myCategory.lower() + "Logged"
        self.password = request.form['ecpassword']
        self.npassword = request.form['ncpassword']
        self.cpassword = request.form['ccpassword']
        result = self.otherRequiredTools.updatePassword(self.mySession, self.password, self.npassword, self.cpassword, self.myCategory)
        if result is True:
            return render_template(self.myCategory.lower() + 'Home.html')
        if result == "Invalid Password":
            return render_template('changePassword.html', errorMessage="The existing password is invalid. Please try again.")
        if result == "Not matching":
            return render_template('changePassword.html', errorMessage="New and Confirm Passwords are not matching.")
    
    def addUser(self):
        return render_template('createEmployee.html')
