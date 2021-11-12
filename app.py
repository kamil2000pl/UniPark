from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'
registeredUser = {}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = '8889'
app.config['MYSQL_USER'] = 'brian'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uniparkdb'
mysql = MySQL(app)


# Forms
class LoginForm(FlaskForm):
    inputEmail = StringField('Email Address', validators=[Email(), InputRequired(), Length(min=8)])
    inputPassword = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    inputFullName = StringField('Full Name', validators=[InputRequired(), Length(min=3)])
    inputEmail = StringField('Email Address', validators=[Email(), InputRequired(), Length(min=8)])
    inputPassword = PasswordField('Password', validators=[InputRequired(), Length(min=8), EqualTo('inputPasswordRepeat', message='Passwords must match')])
    inputPasswordRepeat = PasswordField('Repeat Password')
    submit = SubmitField('Register')


# ROUTES NOT CORRECT, JUST DOING BELOW TO VIEW WEBPAGES QUICKLY


@app.route('/')
def index():
    return render_template("index.html")


# FIX HERE
@app.route('/register', methods=["GET", "POST"])
def register():
    msg = ""
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        fullname = form.inputFullName.data
        email = form.inputEmail.data
        hashed_password = generate_password_hash(form.inputPassword.data, method="sha256")
        password = hashed_password

        # Create Cursor
        cur = mysql.connection.cursor()

        # Check if email already exists in db
        cur.execute("SELECT * FROM users WHERE email_address = %s", email)
        check_email = cur.fetchone()

        if check_email:
            msg = "Email already exists"
        else:
            # Execute
            cur.execute("INSERT INTO users(full_name, email_address, password) VALUES(%s, %s, %s)",
                        (fullname, email, password))
            # Commit to DB
            mysql.connection.commit()
            # Close connection
            cur.close()
            flash('the task created ', 'success')

# post them to db - below just testing login / reg without db
# registeredUser["fullName"] = form.inputFullName.data
# registeredUser["email"] = form.inputEmail.data
# hashed_password = generate_password_hash(form.inputPassword.data, method="sha256")
# registeredUser["password"] = hashed_password

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.inputEmail.data
        password = form.inputPassword.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Check if email already exists in db
        # might need to check password hash here will test later
        cur.execute("SELECT * FROM users WHERE email_address = %s AND password = %s", email, password)
        check_account = cur.fetchone()

        if check_account:
            msg = "Logged in successfully"
            return redirect(url_for("user_dashboard"))
        else:
            msg = "Incorrect Details"
    else:
        return render_template("login.html", form=form)


@app.route('/user')
def user_dashboard():
    return render_template("user_dashboard.html")


@app.route('/user_manage_account')
def user_manage_account():
    return render_template("user_manage_account.html")


@app.route('/user_manage_car')
def user_manage_car():
    return render_template("user_manage_car.html")


@app.route('/user_card_payment_details')
def user_card_payment_details():
    return render_template("user_card_payment_details.html")


@app.route('/user_top_up_account')
def user_top_up_account():
    return render_template("user_top_up_account.html")


@app.route('/kiosk')
def kiosk():
    return render_template("kiosk.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
