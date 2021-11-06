from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, data_required, Email, Length, DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'
formData = {}


# Forms
class LoginForm(FlaskForm):
    inputEmail = StringField('Email Address', validators=[InputRequired(), Length(min=8, max=80), Email()])
    inputPassword = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80, message="minimum 8 chars")])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    inputFullName = StringField('Full Name', validators=[InputRequired(), Length(min=8, max=80)])
    inputEmail = StringField('Email Address', validators=[InputRequired(), Length(min=8, max=80), Email()])
    inputPassword = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80, message="minimum 8 chars"), EqualTo('inputPasswordRepeat', message='Passwords must match')])
    inputPasswordRepeat = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

# ROUTES NOT CORRECT, JUST DOING BELOW TO VIEW WEBPAGES QUICKLY


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.inputEmail.data + ' ' + form.inputPassword.data + '</h1>'
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.inputEmail.data + ' ' + form.inputPassword.data + '</h1>'
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
