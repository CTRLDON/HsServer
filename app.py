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
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


# get the local network Ip address

def retrieve_ip():
    soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    soc.connect(('8.8.8.8',80))
    ip = soc.getsockname()[0]
    soc.close()
    return ip

# create a server class for defining Flask application
def flask_creation():
    app = Flask(__name__) # creating a Flask object
    lm = LoginManager()
    lm.init_app(app) # on initilization of the server object trigger this function
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db" # creating a URI for users database
    app.secret_key = "cc6e169f370f521ac2d5a301caf06c57af57cecfa67c05a1437f2aee10e9681e" # secret key for hashing
    db = SQLAlchemy(app) # creating SQLAlchemy object for handling the database   

    class User(db.Model): # creaing a users class for making a basic template of each user
        id:Mapped[int] = mapped_column(primary_key=True) # special ID for each user
        username:Mapped[str] = mapped_column(unique=True,nullable=False) # making the username unique for each user
        email:Mapped[str] = mapped_column(nullable=False)# email address field
        password:Mapped[str] = mapped_column(nullable=False) # password hash saved
    
    with app.app_context():
        db.create_all() # setting up the database on app context

    @app.route('/')
    # @login_required
    def index():
        return render_template("homePage.html") # rendering home page
    
    @lm.user_loader
    def load_user(userId):
        return User.query.get(userId)
    @app.route('/signup' , methods=['POST','GET'])
    def sign_up():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            pm = PasswordHasher()
            hashed_pass = pm.hash(password)
            new_user = User(username=username,password=hashed_pass,email=email)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('user_files',username=username))
        return render_template('register.html')
    
    @app.route('/login' , methods=['POST','GET'])
    def login():
        if request.method == 'POST':
            login_name = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            pm = PasswordHasher()
            hashed_pass = pm.hash(password)
            user = db.get_or_404(User,login_name)
            if user.password == hashed_pass:
                return redirect(url_for('user_files',username=user.username))
            else:
                render_template('login.html')

        return render_template('login.html')


    @app.route('/files/<username>')
    def user_files(username):
        return render_template('files.html',username=username)
    
    
    return app



if __name__ == '__main__':
    ip_address = retrieve_ip()
    ser = flask_creation()
    ser.run(host=ip_address or 'localhost',port=5050)