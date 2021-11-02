from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ROUTES NOT CORRECT, JUST DOING BELOW TO VIEW WEBPAGES QUICKLY


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/user')
def user_dashboard():
    return render_template("user_dashboard.html")


@app.route('/user_manage_account')
def user_manage_account():
    return render_template("user_manage_account.html")


@app.route('/user_manage_car')
def user_manage_car():
    return render_template("user_manage_car.html")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
