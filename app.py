# importing all the nessecary things from flask
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file,
    send_from_directory,
    session,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required
from sqlalchemy import Integer , String , select
from sqlalchemy.orm import Mapped , mapped_column
from os import mkdir,path
import socket
import re
from utils import login_status,set_session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


# get the local network Ip address

def retrieve_ip():
    soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    soc.connect(('8.8.8.8',80))
    ip = soc.getsockname()[0]
    soc.close()
    return ip

# create a server functiion for defining Flask application
def flask_creation():
    app = Flask(__name__) # creating a Flask object
    lm = LoginManager() # creating a password manager object
    lm.init_app(app) # on initilization of the server object trigger this function
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db" # creating a URI for users database
    app.secret_key = "cc6e169f370f521ac2d5a301caf06c57af57cecfa67c05a1437f2aee10e9681e" # secret key for hashing
    db = SQLAlchemy(app) # creating SQLAlchemy object for handling the database   

    class User(db.Model): # creaing a users class for making a basic template of each user
        id:Mapped[int] = mapped_column(primary_key=True) # special ID for each user
        username:Mapped[str] = mapped_column(unique=True,nullable=False) # making the username unique for each user
        email:Mapped[str] = mapped_column(nullable=False)# email address field
        password:Mapped[str] = mapped_column(nullable=False) # password hash saved
        user_id:Mapped[str] = mapped_column(nullable=False)
    
    with app.app_context():
        db.create_all() # setting up the database on app context

    @app.route('/')
    @login_status
    def index():
        return render_template("homePage.html") # rendering home page
    
    @lm.user_loader
    def load_user(userId):
        return User.query.get(userId)
    

    @app.route('/signup' , methods=['POST','GET'])
    def sign_up():
        if request.method == 'POST': # checking the the method type
            username = request.form.get('username') # getting the username from the form section
            password = request.form.get('password') # getting the password entered from the user
            email = request.form.get('email') # getting the email address from the user
            pm = PasswordHasher() # setting up password hashing object
            hashed_pass = pm.hash(password , salt=None) # hashing the entered password to save in the database
            uid = hashed_pass[len(hashed_pass)-6:] # getting a special user id from the last 6 characters
            new_user = User(username=username,password=hashed_pass,email=email , user_id = uid) # saving the data of the user in a User object
            db.session.add(new_user) # adding the user in the database
            db.session.commit() # saving the changes
            
            return redirect(url_for('user_files',uid=uid)) # redirecting to the files page of this user
        return render_template('register.html') # rendering the register page if the method is GET
    
    @app.route('/login' , methods=['POST','GET'])
    def login():
        if request.method == 'POST':
            login_name = request.form.get('username') # getting the username from the form
            password = request.form.get('password') # getting the password from the form
            remember = request.form.get('save-info')
            # email = request.form.get('email')
            pm = PasswordHasher() # the hashing object
            # hashed_pass = pm.hash(password,salt=None)

            user = db.session.execute(select(User).filter_by(username=login_name)) # searching first for the user in the database
            user = user.scalar() # converting the returned data to a list
            if user == None:
                return render_template('login.html' , error_msg = "username or password is incorrect")
            
            if remember == "on":
                session['username'] = login_name
                session['user_id'] = user.user_id
            # print(hashed_pass)
            try:
                pm.verify(user.password , password) # checking if the password related the retrieved user matches the entered password hash
                return redirect(url_for('user_files',uid=user.user_id)) # if true it will redirect to the files page of the user
            except VerifyMismatchError:
                return render_template('login.html' , error_msg = "username or password is incorrect") # else it will get back again (for now but in the future it will send a message to the user in the website)

        return render_template('login.html')


    @app.route('/files/<uid>')
    def user_files(uid):
        user = db.session.execute(select(User).where(User.user_id == uid)).scalar() # selecting a user based on the user_id provided
        return render_template('files.html',username=user.username) # rendering the page
    
    
    return app



if __name__ == '__main__':
    ip_address = retrieve_ip()
    ser = flask_creation()
    ser.run(host=ip_address or 'localhost',port=5050)