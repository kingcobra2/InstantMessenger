from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_required, login_user, current_user, login_required, logout_user
from wtforms_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretketthatnooneknows'

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
    return render_template("index.html", form = reg_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    #Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

        return "Not logged in :("

    return render_template("login.html", form=login_form)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if current_user.is_authenticated:
        return "Chat with me."
    return "Please login before entering a chat"
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return "Logged out using flask login"

    
if __name__ == "__main__":
    
    app.run(debug=True)


