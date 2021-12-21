from flask import Flask, render_template, request, flash, session
import database

app = Flask(__name__)


@app.route('/')
def select_post():
    return render_template('select_post.html')


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/buyer_login')
def buyer_login():
    return render_template('buyer_login_signup.html')

@app.route('/employee_login')
def employee_login():
    return render_template('employee_login.html')

@app.route('/Sign_up_Buyer')
def sign_up_Buyer():
    return render_template('Sign_up3.html')

@app.route('/Sign_up_Employee')
def sign_up_Employee():
    return render_template('Sign_up_Employee.html')

@app.route('/add_user_cred', methods=["GET", "POST"])
def add_user_cred():
    email_c = request.form['Email']
    f_name = request.form['fname']
    l_name = request.form['lname']
    NAME = f_name+l_name
    ph_number = request.form['PhNumber']
    PSWT = request.form['pswt']
    PSW = request.form['psw']
    if (PSWT == PSW):
        PASS = PSW
    POST = request.form['POST']
    database.sign_up(email_c,NAME,ph_number,PASS,POST)
    return "SIGNED UP successfully, Work-in-progress ahead"


@app.route('/admin_login_validation', methods=["GET", "POST"])
def admin_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Admin'
    is_valid = database.validate_login(email, password, post)

    if is_valid:
        # flash("You are successfuly logged in!")
        # if request.method == "POST":
           # session.permanent = True
           # session["email"] = email
        return render_template('admin_home.html')

    # flash("email/password is incorrect!")
    return "LOGIN FAILED"

@app.route('/buyer_login_validation', methods=["GET", "POST"])
def buyer_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Buyer'
    is_valid = database.validate_login(email, password, post)

    if is_valid:
        # flash("You are successfuly logged in!")
        # if request.method == "POST":
           # session.permanent = True
           # session["email"] = email
        return render_template('select_post.html')

    # flash("email/password is incorrect!")
    return "LOGIN FAILED"

@app.route('/employee_login_validation', methods=["GET", "POST"])
def employee_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Employee'
    is_valid = database.validate_login(email, password, post)

    if is_valid:
        # flash("You are successfuly logged in!")
        # if request.method == "POST":
           # session.permanent = True
           # session["email"] = email
        return render_template('select_post.html')

    # flash("email/password is incorrect!")
    return "LOGIN FAILED"


if __name__ == "__main__":
    app.run()  # host="0.0.0.0", port=5000