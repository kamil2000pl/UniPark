from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'

#config = {
#    'user': 'brian',
#    'password': 'brianmckenna',
#    'host': 'localhost',
#    'port': 8889,
#    'database': 'uniparkdb',
#    'raise_on_warnings': True,
#}

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
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
    inputPassword = PasswordField('Password', validators=[InputRequired(), Length(min=8), EqualTo('inputPasswordRepeat',
                                                                                                  message='Passwords must match')])
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
        query = "SELECT * FROM account WHERE email_address = %s"

        cursor.execute(query, value)
        check_email = cursor.fetchone()

        if check_email:  # if the email already exists
            msg = "Email already exists"
            print(msg)
        else:  # if the email does not exist we can then proceed to adding the account
            add_account = "INSERT INTO account(account_balance, email_address, password) VALUES (%s, %s, %s)"  # account id auto created and incremented
            account_data = (0.00, email, password)
            print(account_data)
            cursor.execute(add_account, account_data)
            account_id = cursor.lastrowid  # gets the account id

            add_user = "INSERT INTO driver (account_id, college_id, full_name) VALUES (%s, %s, %s)"
            user_data = (account_id, "", fullname)  # college_id need a default value?
            # Execute
            cursor.execute(add_user, user_data)
            # Commit to DB
            cnx.commit()
            # Close Cursor & connection
            cursor.close()
            cnx.close()

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.inputEmail.data
        password = form.inputPassword.data

        account_query = "SELECT * FROM account WHERE email_address = %s"
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
    cursor.close()


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
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        return render_template("user_dashboard.html", account=account, session=session, user=user)
    return redirect(url_for('login'))


@app.route('/user_manage_account')
def user_manage_account():
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        car = get_car_details()
        return render_template("user_manage_account.html", account=account, session=session, user=user, car=car)
    return redirect(url_for('login'))


@app.route('/user_manage_account_personal_details')
def user_manage_account_personal_details():
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        return render_template("user_manage_account_personal_details.html", account=account, session=session, user=user)
    return redirect(url_for('login'))


@app.route('/user_manage_car')
def user_manage_car():
    if 'loggedin' in session:
        car = get_car_details()
        return render_template("user_manage_car.html", car=car)
    return redirect(url_for('login'))


@app.route('/user_manage_car/add_car', methods=["GET", "POST"])
def user_add_car():
    vehicle_reg = request.form['vehicleReg'].upper()
    if 'loggedin' in session:
        car_details = get_car_details()
        print(car_details)
        # add cars
        account = get_account_details()
        add_car(account[0], vehicle_reg)
        return redirect(url_for('user_manage_car'))
    return redirect(url_for('login'))


@app.route('/user_manage_car/delete_car', methods=["GET", "POST"])
def user_delete_car():
    vehicle_reg = request.form['vehicle_reg']
    if 'loggedin' in session:
        delete_car = "DELETE FROM car WHERE registration = %s"
        values = (vehicle_reg,)
        cursor.execute(delete_car, values)
        cnx.commit()
        return redirect(url_for('user_manage_car'))
    return redirect(url_for('login'))


@app.route('/user_card_payment_details')
def user_card_payment_details():
    return render_template("user_card_payment_details.html")


@app.route('/user_top_up_account')
def user_top_up_account():
    return render_template("user_top_up_account.html")


@app.route('/kiosk')
def kiosk():
    return render_template("kiosk.html")


@app.route('/kiosk/print_ticket', methods=["GET", "POST"])
def kiosk_print_ticket():
    print_request = request.form['kiosk_print_ticket']
    generate_datetime = datetime.datetime.now()
    if print_request:
        ticket_obj = generate_datetime
        print("Ticket Object Created!")
        print(ticket_obj)
        return render_template("kiosk.html", ticket_obj=ticket_obj)
    return render_template("kiosk.html")


def get_account_details():
    account_query = "SELECT * FROM account WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(account_query, values)
    account = cursor.fetchone()
    return account


def get_user_details():
    user_query = "SELECT * FROM driver WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(user_query, values)
    user = cursor.fetchone()
    return user


def get_car_details():
    user_query = "SELECT * FROM car WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(user_query, values)
    # fetch one car atm
    car_details = cursor.fetchall()
    return car_details


# create a function that will add car to the db

def add_car(account_id, vehicle_reg):
    # check the car isn't registered already
    check_car_query = "SELECT COUNT(registration) FROM car WHERE registration = %s"
    values = (vehicle_reg,)  # input from form on manage car details page
    cursor.execute(check_car_query, values)
    result = cursor.fetchone()
    print(result)
    if result[0] == 0:
        insert_car = "INSERT INTO car VALUES (%s, %s)"
        values = (vehicle_reg, account_id)
        cursor.execute(insert_car, values)
        # Commit to DB
        cnx.commit()
        print(cursor.rowcount, "was inserted.")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
