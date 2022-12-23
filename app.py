from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
import os


from flask import Flask, render_template, request, Response, jsonify, redirect, url_for, session
import database as dbase  
from User import User
from Emp import Emp

db = dbase.dbConnection()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# def get_current_user():
#     user = None
#     if 'user' in session:
#         user = session['user']
#         user = db['users']
#         userReceived = user.find()
#     return user


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/login', methods = ["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        users = db['users']
        login_user = users.find_one({'name':name, 'password':password})
        if login_user:
                session['user'] = name
                return redirect(url_for('dashboard'))
        else:
            error = 'Username or password did not match, Try again.'
    return render_template('login.html', loginerror = error)


@app.route('/register', methods=["POST", "GET"])
def register():

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        users = db['users']
        existing_user = users.find_one({'name':name})

        if existing_user:
            return render_template('register.html', registererror = 'Username already exist , try different username.')
        
        users.insert_one({'name': name, 'password': password})
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    emps = db['emps']
    allemp = emps.find()
    return render_template('dashboard.html', allemp = allemp)

@app.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    if request.method == "POST":
        emps = db['emps']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        if name and email and phone and address:
            emp = Emp(name, email, phone, address, 1,1,1,1)
            emps.insert_one(emp.toDBCollectionEmp())
            return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html')

@app.route('/fetchone/<string:phone>')
def fetchone(phone):
    emp = db['emps']
    single_emp = emp.find_one({'phone':phone})
    return render_template('updateemployee.html', single_emp = single_emp)

@app.route('/updateemployee' , methods = ["POST", "GET"])
def updateemployee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        if name and email and phone and address:
            emp = db['emps']
            emp.update_one({'phone':phone},{'$set': {'name': name, 'email': email, 'phone': phone, 'address': address}} )
            return redirect(url_for('dashboard'))
    return render_template('updateemployee.html')

@app.route('/deleteemp/<string:phone>', methods = ["GET", "POST"])
def deleteemp(phone):
    if request.method == 'GET':
        emp = db['emps']
        emp.delete_one({'phone':phone})
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')


@app.route('/singleemployee/<string:phone>')
def singleemployee(phone):
    emp = db['emps']
    single_emp = emp.find_one({'phone':phone})
    return render_template('singleemployee.html', single_emp = single_emp)

@app.route('/searchemployee', methods = ["POST", "GET"])
def searchemployee():
    if request.method == 'POST':
        key = request.form['key']
        emp = db['emps']
        searchemp = emp.find({'name':key})
        return render_template('searchemployee.html', searchemp = searchemp, key=key)    
    return render_template('searchemployee.html')

@app.route('/logout')
def logout():
    session['user'] = None
    return render_template('login.html')

if __name__ == '__main__':
    HOST = "0.0.0.0"
    PORT = os.environ.get('FLASK_PORT') or 8080
    DEBUG = True
    app.run(HOST, PORT, DEBUG)
