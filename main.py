from flask import Flask, render_template

from wtforms_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretketthatnooneknows'

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hhotlmfiiwsiiy:260d205aa0069230cad9ad9c7f1d8d95621b696991131c72249f18b3c150580f@ec2-3-92-98-129.compute-1.amazonaws.com:5432/d975kirgq1gbrq'
db = SQLAlchemy(app)


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has this username!"

        #Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return "Inserted into DB!"
    return render_template("index.html", form = reg_form)



if __name__ == "__main__":
    
    app.run(debug=True)


