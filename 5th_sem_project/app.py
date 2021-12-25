from os import name
from flask import Flask, render_template, request, flash, session
import database


app = Flask(__name__)


@app.route('/')
def select_post():
    return render_template('select_post.html')

@app.route('/admin_login')
def admin_home():
    return render_template('admin_login.html')

@app.route('/admin_home')
def admin_login():
    return render_template('admin_home.html')

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

arr = database.Database_common_operations.run_query_and_return_all_data("select * from user_details where post == 'Employee';")
te = 0
temp = []
for x in arr:
    ID = arr[te][0]
    Ename = arr[te][2]
    PhNumber = arr[te][3]
    ar = [ID,Ename,PhNumber]
    temp.append(ar)
    te += 1

print(te)


@app.route('/Manage_Employees')
def Manage_Employees():
    return render_template('Manage_Employees.html',ARRAY = temp,length = te-1,NAME = name)


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
    query = database.Database_common_operations.run_query_and_return_all_data(f"select user_details_name from user_details where email == '{email}';")
    global name
    name = query[0][0]
    if is_valid:
        # flash("You are successfuly logged in!")
        # if request.method == "POST":
           # session.permanent = True
           # session["email"] = email
        return render_template('admin_home.html',NAME = name)

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

@app.route('/edit_employee',methods=["GET", "POST"])
def edit_employee():
    if request.method == "POST":
        R_ID = request.form.get('r_id')
        print(R_ID)
    return "DONE"

if __name__ == "__main__":
    app.run()  # host="0.0.0.0", port=5000