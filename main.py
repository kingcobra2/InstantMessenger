from time import localtime, strftime
from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_required, login_user, current_user, login_required, logout_user
from wtforms_fields import *
from models import *
from flask_socketio import SocketIO, send, emit, join_room, leave_room

# Configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretketthatnooneknows'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize flask-socketio
socketio = SocketIO(app)

ROOMS = ["lounge", "news", "games", "coding"]


#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hhotlmfiiwsiiy:260d205aa0069230cad9ad9c7f1d8d95621b696991131c72249f18b3c150580f@ec2-3-92-98-129.compute-1.amazonaws.com:5432/d975kirgq1gbrq'
db = SQLAlchemy(app)

#Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        #Add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("index.html", form=reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    #Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))


    return render_template("login.html", form=login_form)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    
   
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return "Logged out using flask login"


@socketio.on('message')
def message(data):

    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp':
     strftime("%b-%d %I:%M%p", localtime())}, room=data['room'])
     
@socketio.on('join')
def join(data):

    join_room(data['room'])
    send({'msg': data['username'] + " has joined the room."}, room=data['room'])

@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " has left the room."}, room=data['room'])



if __name__ == "__main__":
    socketio.run(app, debug=True)


