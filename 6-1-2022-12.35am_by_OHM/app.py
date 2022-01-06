from os import name
from flask import Flask, render_template, request, flash, session, redirect
import database

app = Flask(__name__)

app.secret_key = "HX5I09WBDSDF" # Any random secret key 

@app.route('/')
def select_post():
    return render_template('index.html')


#####################################################
#   Admin login, validation and logout 
#####################################################


@app.route('/admin_login')
def admin_home():
    return render_template('admin_login.html')


@app.route('/admin_login_validation', methods=["GET", "POST"])
def admin_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Admin'
    is_valid = database.validate_login(email, password, post)
    query = database.Database_common_operations.run_query_and_return_all_data(
        f"select user_details_name from user_details where email == '{email}';")
    global name
    name = query[0][0]
    if is_valid:
        global numEmp
        session['Admin'] = name

        return redirect('/admin_home')
    flash("email/password is incorrect!")
    return redirect('/admin_login')


@app.route('/logout')
def logout():
    # Session unset 
    session.pop("Admin", None)
    return render_template('admin_login.html')



#####################################################
#   Admin Panel Operations
#####################################################


@app.route('/admin_home')
def admin_login():
    
    if not 'Admin' in session:
        return redirect('/admin_login')

    numEmp_ = database.getNumberOfEmployee()
    NumberOfProducts_ = database.getNumberOfProducts()
    NumberOfOrders_ = database.getNumberOfPendingOrders()
    NumberOfSuppliers_ = database.getNumberOfSupplier()
    return render_template('admin_home.html', NAME=session['Admin'], 
        NumberOfEmployee=numEmp_, NumberOfProducts=NumberOfProducts_, 
        NumberOfOrder=NumberOfOrders_, NumberOfSuppliers=NumberOfSuppliers_)


@app.route('/Sign_up_Employee')
def sign_up_Employee():
    return render_template('employee_signup.html')


@app.route('/Manage_Employees')
def Manage_Employees():

    if not 'Admin' in session:  
        return redirect('/admin_login')

    arr = database.Database_common_operations.run_query_and_return_all_data(
        "select * from user_details where post == 'Employee';")
    te = 0
    temp = []
    for x in arr:
        ID = arr[te][0]
        Ename = arr[te][2]
        PhNumber = arr[te][3]
        ar = [ID, Ename, PhNumber]
        temp.append(ar)
        te += 1

    return render_template('Manage_Employees.html', ARRAY=temp, length=te - 1, NAME=name)


@app.route('/add_new_employee', methods=["GET", "POST"])
def add_new_employee():

    if not 'Admin' in session:
        return redirect('/admin_login')
    
    email_c = request.form['Email']
    f_name = request.form['fname']
    ph_number = request.form['PhNumber']
    PSWT = request.form['pswt']
    PSW = request.form['psw']
    POST = 'Employee'
    if PSWT == PSW:
        PASS = PSW
    else:
        print(PSW)
        print(PSWT)
        return redirect('/Sign_up_Employee')
    opt_number = request.form['PhNumber2']
    Gender = request.form['Gender']
    B_date = request.form['DOB']
    print(B_date)
    Address = request.form['Address']
    State = request.form['countrya']
    City = request.form['district']
    res = database.sign_up(email_c, f_name, ph_number, PASS, POST, Gender, B_date, Address, opt_number, City, State)
    return redirect('/Manage_Employees')


"""
Product related operations 
"""

@app.route('/edit_product_inventory/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory(pid):

    if not 'Admin' in session:
        return redirect('/admin_login')


    return render_template('edit_product_inventory.html',PID = pid)

@app.route('/add_new_product')
def add_product():
    return render_template('add_product.html')

@app.route('/edit_product_details/<string:pid>', methods=["GET", "POST"])
def edit_product_details(pid):

    if not 'Admin' in session:
        return redirect('/admin_login')

    id = pid
    p_name = request.form['P_Name']

    rate = request.form['Rate']
    weight = request.form['Weight']
    w_unit = request.form['w_unit']
    desc = request.form['P_desc']
    cate = request.form['cate']
    dimen = request.form['Dimension']
    placement = request.form['Placement_In_Warehouse']
    lower_bound = request.form['lower_bound']
    database.edit_product_details(id,p_name,rate,weight,w_unit,desc,cate,dimen,placement,lower_bound)
    print("REACHED")

    return redirect('/manage_products')



@app.route('/more_product_details/<string:pid>', methods=["GET", "POST"])
def more_product_details(pid):

    if not 'Admin' in session:
        return redirect('/admin_login')

    return "More Product Details"


@app.route('/manage_products')
def manage_employe():

    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getMainProductData()
    return render_template('manage_products.html', NAME=name, data=data)


@app.route('/manage_suppliers')
def manage_suppliers():

    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getAllSuppliers()
    return render_template('manage_supplier.html', NAME=name, data=data)



@app.route('/add_new_supplier')
def add_new_supplier():

    if not 'Admin' in session:
        return redirect('/admin_login')

    return render_template('add_new_supplier.html')


@app.route('/add_new_supplier_action', methods=["GET", "POST"])
def add_new_employee_action():

    name = request.form['fname']
    email = request.form['Email']
    phone = request.form['PhNumber']
    company_name = request.form['company_name']
    product_id = request.form['product_id']
    address = request.form['Address']
    database.add_supplier(name, phone, address, email, company_name, product_id)
    return redirect('/manage_suppliers')


@app.route('/remove_supplier/<string:sid>', methods=["GET", "POST"])
def remove_supplier(sid):

    if not 'Admin' in session:
        return redirect('/admin_login')

    database.removeSupplier(sid)
    return redirect('/manage_suppliers')



@app.route('/edit_employee/<string:id>', methods=["GET", "POST"])
def edit_employee(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    database.remove_user(id)
    return redirect('/Manage_Employees')


@app.route('/employee_details/<string:id>', methods=["GET", "POST"])
def employee_details(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    details = database.getEmployeeDetails(id)
    details = details[0]
    login_history = database.getEmployeeLoginHistory(id)
    return render_template('employee_details_manage_employee.html', x=details, history=login_history, NAME=name)



# Admin Details 
@app.route('/your_details')
def your_details():
    data1 = database.getAdminDetails(session['Admin'])
    id_ = database.getAdminID(session['Admin'])
    data2 = database.getAdminLoginHistory(id_)
    return render_template('admin_profile.html', NAME=session['Admin'], data1=data1, data2=data2)


@app.route('/edit_product_inventory_action/<string:pid>', methods=["GET", "POST"])
def edit_product_inventory_action(pid):
    quantity = request.form["quantity"]
    operation = request.form["operation"]
    database.editProductInventory(quantity, operation,pid)
    return redirect('/manage_products')

@app.route('/edit_products/<string:id>', methods=["GET", "POST"])
def edit_products(id):
    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getDetailedProductsData(id)
    category = database.getCategory()
    return render_template('edit_products.html',NAME = name, data = data, category = category)

@app.route('/manage_orders')
def manage_orders():
    data = database.getAllOrdersDetails()
    return render_template('manage_orders.html', NAME=session['Admin'], data=data)


#####################################################
#   Employee related Operations
#####################################################



@app.route('/employee_login')
def employee_login():
    return render_template('employee_login.html')


@app.route('/employee_login_validation', methods=["GET", "POST"])
def employee_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Employee'
    is_valid = database.validate_login(email, password, post)

    if is_valid:
        return render_template('select_post.html')

    
    return "LOGIN FAILED"



#####################################################
#   Buyer related Operations
#####################################################



@app.route('/buyer_login')
def buyer_login():
    return render_template('buyer_login.html')


@app.route('/buyer_sign_up')
def sign_up_Buyer():
    return render_template('/buyer_sign_up.html')

@app.route('/add_buyer', methods=["GET", "POST"])
def add_buyer():
    email_c = request.form['Email']
    f_name = request.form['fname']
    ph_number = request.form['PhNumber']
    PSWT = request.form['pswt']
    PSW = request.form['psw']
    POST = 'Buyer'
    if PSWT == PSW:
        PASS = PSW
    else:
        print(PSW)
        print(PSWT)
        return redirect('/buyer_sign_up')
    opt_number = request.form['PhNumber2']
    Gender = request.form['Gender']
    B_date = request.form['DOB']
    print(B_date)
    Address = request.form['Address']
    State = request.form['countrya']
    City = request.form['district']
    """
email: str, user_name: str, ph_number, password: str, post: str, gender: str, birth: str, address: str,
 city: str, state: str,opt_number = 0
"""
    res = database.sign_up(email_c, f_name, ph_number, PASS, POST, Gender, B_date, Address, City, State, opt_number)
    return redirect('/')


@app.route('/buyer_login_validation', methods=["GET", "POST"])
def buyer_login_validate():
    email = request.form['email']
    password = request.form['psw']
    post = 'Buyer'
    is_valid = database.validate_login(email, password, post)
    if is_valid:
        return "Buyer_Login_Successfully"
    return "LOGIN FAILED"

@app.route('/manage_buyers')
def manage_buyers():
    if not 'Admin' in session:
        return redirect('/admin_login')

    data = database.getBuyerDetails()
    return  render_template('manage_buyers.html', NAME=name, data=data)



if __name__ == "__main__":
    app.run()  # host="0.0.0.0", port=5000
