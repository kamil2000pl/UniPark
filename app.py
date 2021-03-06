from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp, DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

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

# config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'port': 3306,
#     'database': 'uniparkdb',
#     'raise_on_warnings': True,
# }

cnx = mysql.connector.connect(**config)


# Forms
class LoginForm(FlaskForm):
    inputEmail = StringField('Email Address', validators=[Email(message="Please enter a valid email address"), InputRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password', validators=[InputRequired(message="Please enter your password"), Regexp("^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$", message="Password must contain a minimum of eight characters, at least one letter and one number")])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    inputFullName = StringField('Full Name', validators=[InputRequired(message="Please enter your full name"), Length(min=3, message="Full name must be at least 3 characters")])
    inputEmail = StringField('Email Address', validators=[Email(message="Please enter a valid email address"), InputRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password', validators=[InputRequired(message="Please enter your password"), EqualTo('inputPasswordRepeat', message='Passwords must match'), Regexp("^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$", message="Password must contain a minimum of eight characters, at least one letter and one number")])
    inputPasswordRepeat = PasswordField('Repeat Password')
    inputCheckBoxTerms = BooleanField(validators=[DataRequired(message="You must agree to terms of service to proceed")])
    submit = SubmitField('Register')


# would have liked to get more validation done on all forms but ran out of time
class CardPaymentDetailsForm(FlaskForm):
    inputNameOnCard = StringField('Name on card', validators=[InputRequired(message="Please enter the name on card"), Length(min=3, message="Name on card must be at least 3 characters")])
    inputCardNumber = StringField('Card number', validators=[InputRequired(message="Please enter the card number"), Regexp("^4[0-9]{12}(?:[0-9]{3})?$", message="Enter a valid card number. Card must begin with 4")])
    inputExpiryDate = StringField('Expiry date', validators=[InputRequired(message="Please enter the expiry date")])
    inputCCV = StringField('CCV', validators=[InputRequired(message="Please enter the CVV number"), Regexp("^[0-9]{3, 4}$", message="CCV must be 3 or 4 digits")])
    submit = SubmitField('Save Card Details')


class VehicleRegForm(FlaskForm):
    inputVehicleReg = StringField('Vehicle Registration', validators=[InputRequired(message="Please enter your vehicle registration")])
    submit = SubmitField('Add Vehicle')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    cursor = cnx.cursor(buffered=True)

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
            flash("Email address already exists")
            return render_template("register.html", form=form)
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

            # need to generate the payment id
            add_payment = "INSERT INTO payment (account_id) VALUES (%s)"
            payment_data = (account_id,)
            cursor.execute(add_payment, payment_data)
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
    cursor = cnx.cursor(buffered=True)

    if request.method == 'POST' and form.validate_on_submit():
        email = form.inputEmail.data
        password = form.inputPassword.data

        account_query = "SELECT * FROM account WHERE email_address = %s"
        values = (email,)
        cursor.execute(account_query, values)
        account = cursor.fetchone()
        cursor.close()
        print(account)

        if not account or not check_password_hash(account[3], password):
            msg = "Unsuccessful Login, try again"
            flash(msg)
            return render_template("login.html", form=form)
        else:
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
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        car = get_car_details()
        payment = get_card_payment_details()
        return render_template("user_dashboard.html", account=account, session=session, user=user, car=car, payment=payment)
    return redirect(url_for('login'))


@app.route('/user_manage_account')
def user_manage_account():
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        car = get_car_details()
        payment = get_card_payment_details()
        return render_template("user_manage_account.html", account=account, session=session, user=user, car=car, payment=payment)
    return redirect(url_for('login'))


@app.route('/user_manage_personal_details')
def user_manage_personal_details():
    if 'loggedin' in session:
        account = get_account_details()
        user = get_user_details()
        car = get_car_details()
        return render_template("manage_personal_details.html", user=user)
    return redirect(url_for('login'))


@app.route('/user_manage_personal_details/add_id', methods=["GET", "POST"])
def user_add_id():
    college_id = request.form['studentId']
    if 'loggedin' in session:
        user_details = get_user_details()
        if user_details[2] == "" or user_details[2] is None:
            add_college_id(user_details[0], college_id)
            return redirect(url_for('user_manage_personal_details'))
        else:
            return redirect(url_for('user_manage_personal_details'))
    return redirect(url_for('login'))


@app.route('/user_manage_personal_details/delete_id', methods=["GET", "POST"])
def user_delete_id():
    cursor = cnx.cursor(buffered=True)
    driver_id = request.form['driver_id']
    if 'loggedin' in session:
        remove_college_id = "UPDATE driver SET college_id = '' WHERE driver_id = %s"
        values = (driver_id,)
        cursor.execute(remove_college_id, values)
        cnx.commit()
        cursor.close()
        return redirect(url_for('user_manage_personal_details'))
    return redirect(url_for('login'))


@app.route('/user_manage_car/')
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
        # add cars
        account = get_account_details()
        add_car(account[0], vehicle_reg)
        return redirect(url_for('user_manage_car'))
    return redirect(url_for('login'))


# add card payment
@app.route('/user_card_payment_details/add_card_payment', methods=["GET", "POST"])
def user_add_card_payment():
    # get the data from the forms
    # need to do validation with wtforms here
    name_on_card = request.form['inputNameOnCard']
    card_number = request.form['inputCardNumber']
    expiry_date = request.form['inputExpiryDate']
    ccv = request.form['inputCCV']
    card_form_requests = [name_on_card, card_number, expiry_date, ccv]

    if 'loggedin' in session:
        account = get_account_details()
        add_card(account, card_form_requests)
        return redirect(url_for('user_card_payment_details'))
    return redirect(url_for('login'))

# create a function that will card payment


def add_card(account, card_form_requests):
    cursor = cnx.cursor(buffered=True)
    insert_card = "UPDATE payment SET name_on_card = %s, card_number = %s, card_expiry = %s, ccv = %s WHERE account_id = %s"
    values = (card_form_requests[0], card_form_requests[1], card_form_requests[2], card_form_requests[3], account[0])
    cursor.execute(insert_card, values)
    # Commit to DB
    cnx.commit()
    cursor.close()
    print(cursor.rowcount, "was inserted.")


@app.route('/user_manage_car/delete_car', methods=["GET", "POST"])
def user_delete_car():
    cursor = cnx.cursor(buffered=True)
    vehicle_reg = request.form['vehicle_reg']
    if 'loggedin' in session:
        delete_car = "DELETE FROM car WHERE registration = %s"
        values = (vehicle_reg,)
        cursor.execute(delete_car, values)
        cnx.commit()
        cursor.close()
        return redirect(url_for('user_manage_car'))
    return redirect(url_for('login'))


@app.route('/user_card_payment_details')
def user_card_payment_details():
    if 'loggedin' in session:
        # get the payment details
        card_payment_details = get_card_payment_details()
        return render_template("user_card_payment_details.html", card_payment_details=card_payment_details)
    return redirect(url_for('login'))


@app.route('/user_top_up_account')
def user_top_up_account():
    if 'loggedin' in session:
        card_payment_details = get_card_payment_details()
        account_details = get_account_details()
        return render_template("user_top_up_account.html", account_details=account_details, card_payment_details=card_payment_details)
    return redirect(url_for('login'))


@app.route('/user_top_up_account/add_funds', methods=["GET", "POST"])
def user_add_funds():
    # get the data from the forms
    name_on_card = request.form['inputNameOnCard']
    card_number = request.form['inputCardNumber']
    expiry_date = request.form['inputExpiryDate']
    ccv = request.form['inputCCV']
    top_up_amount = request.form['inputAmount']
    top_up_account_request = [name_on_card, card_number, expiry_date, ccv, top_up_amount]

    if 'loggedin' in session:
        card_payment_details = get_card_payment_details()
        account_details = get_account_details()
        add_funds(card_payment_details, top_up_account_request)
        return redirect(url_for('user_top_up_account'))
    return redirect(url_for('login'))


def add_funds(card_payment_details, top_up_account_request):
    cursor = cnx.cursor(buffered=True)
    insert_funds = "UPDATE account SET account_balance = account_balance + %s WHERE account_id = %s"
    values = (top_up_account_request[4], card_payment_details[1])
    cursor.execute(insert_funds, values)
    # Commit to DB
    cnx.commit()
    print(cursor.rowcount, "was inserted.")
    cursor.close()


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
    cursor = cnx.cursor(buffered=True)
    account_query = "SELECT * FROM account WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(account_query, values)
    account = cursor.fetchone()
    cursor.close()
    return account


def get_user_details():
    cursor = cnx.cursor(buffered=True)
    user_query = "SELECT * FROM driver WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(user_query, values)
    user = cursor.fetchone()
    cursor.close()
    return user


def get_car_details():
    cursor = cnx.cursor(buffered=True)
    user_query = "SELECT * FROM car WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(user_query, values)
    # fetch one car atm
    car_details = cursor.fetchall()
    cursor.close()
    return car_details


def get_card_payment_details():
    cursor = cnx.cursor(buffered=True)
    card_payment_query = "SELECT * FROM payment WHERE account_id = %s"
    values = (session['id'],)
    cursor.execute(card_payment_query, values)
    card_payment_result = cursor.fetchone()
    cursor.close()
    return card_payment_result


# create a function that will add car to the db

def add_car(account_id, vehicle_reg):
    # check the car isn't registered already
    cursor = cnx.cursor(buffered=True)
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
        flash("Car registration added successfully")
        cursor.close()


# create a function that will add student id to the db

def add_college_id(user_id, college_id):
    # check if add_college_id exists in driver
    cursor = cnx.cursor(buffered=True)
    check_college_id_query = "SELECT COUNT(college_id) FROM driver WHERE college_id = %s"
    values = (college_id,)  # input from form on manage personal details page
    cursor.execute(check_college_id_query, values)
    result = cursor.fetchone()
    if result[0] == 0:
        insert_college_id = "UPDATE driver SET college_id = %s WHERE driver_id = %s"
        values = (college_id, user_id)
        cursor.execute(insert_college_id, values)
        # Commit to DB
        cnx.commit()
        print(cursor.rowcount, "was inserted.")
        cursor.close()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
