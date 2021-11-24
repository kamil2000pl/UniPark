from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'

config = {
    'user': 'brian',
    'password': 'brianmckenna',
    'host': 'localhost',
    'port': 8889,
    'database': 'uniparkdb',
    'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)


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


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        fullname = form.inputFullName.data
        email = form.inputEmail.data
        hashed_password = generate_password_hash(form.inputPassword.data, method="sha256")
        password = hashed_password

        # Check if email already exists in db
        value = (email,)
        query = "SELECT * FROM accounts WHERE email_address = %s"

        cursor.execute(query, value)
        check_email = cursor.fetchone()

        if check_email:  # if the email already exists
            msg = "Email already exists"
            print(msg)
        else:  # if the email does not exist we can then proceed to adding the account
            add_account = "INSERT INTO accounts(account_balance, email_address, password) VALUES (%s, %s, %s)"  # account id auto created and incremented
            account_data = (0.00, email, password)
            print(account_data)
            cursor.execute(add_account, account_data)
            account_id = cursor.lastrowid  # gets the account id

            add_user = "INSERT INTO users (account_id, college_id, full_name) VALUES (%s, %s, %s)"
            user_data = (account_id, "", fullname)  # college_id need a default value?
            # Execute
            cursor.execute(add_user, user_data)
            # Commit to DB
            cnx.commit()
            # Close Cursor & connection
            cursor.close()

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.inputEmail.data
        password = form.inputPassword.data

        account_query = "SELECT * FROM accounts WHERE email_address = %s"
        values = (email,)
        cursor.execute(account_query, values)
        account = cursor.fetchone()
        print(account)

        if not account or not check_password_hash(account[3], password):
            msg = "Unsuccessful Login!"
            return render_template("login.html", form=form)
        else:
            msg = "Logged in successfully"
            session['loggedin'] = True
            session['id'] = account[0]
            return redirect(url_for("user_dashboard"))
    else:
        return render_template("login.html", form=form)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def user_dashboard():
    # check if user is logged in

    if 'loggedin' in session:
        account_query = "SELECT * FROM accounts WHERE account_id = %s"
        values = (session['id'],)
        cursor.execute(account_query, values)
        account = cursor.fetchone()
        print(account)
        return render_template("user_dashboard.html", account=account, session=session)
    return redirect(url_for('login'))


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
