from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps 
from flask_mysqldb import MySQL
import datetime, time
app = Flask(__name__, static_url_path='/static')


# Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'hrmanager'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
 
mysql = MySQL(app)

def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unautharized, Please Login', 'danger')
			return redirect(url_for('login'))
	return wrap

def is_admin_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'admin_logged_in' in session:
			return f(*args, **kwargs)
		elif 'logged_in' in session:
			flash('Unautharized, You are not an admin', 'danger')
			return redirect(url_for('dashboard'))
		else:
			flash('Unautharized, Please Login', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/dashboard')
@is_logged_in
def dashboard():
	return render_template('dashboard.html')


@app.route('/employee/view')
@is_admin_logged_in
def view_employee():
	return render_template('view_employee.html')

@app.route('/attendance')
@is_admin_logged_in
def attendance():
	return render_template('attendance.html')

@app.route('/incentive')
@is_admin_logged_in
def incentive():
	return render_template('incentive.html')

@app.route('/salary')
@is_admin_logged_in
def salary():
	return render_template('salary.html')

@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/profile')
@is_logged_in
def profile():
	return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		emp_id = request.form['emp_id']
		password_candidate = request.form['password']

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			data = cur.fetchone()
			password = data['password']
			if sha256_crypt.verify(password_candidate, password):
				error='Logged in succesfully'
				session['logged_in'] = True
				session['emp_id'] = emp_id
				session['name'] = data['name']
				app.logger.info(data['name'])
				if data['admin'] == 1:
					session['admin_logged_in'] = True
					flash('You are now loged in as an Admin', 'success')
				else:
					flash('You are now loged in as an employee', 'success')
				return redirect(url_for('dashboard'))
			else:
				error='Password does not match, If you don\'t remember Click Forgot Password'
				return render_template('login.html', error=error)
		else:
			error='Employee id not found'
			return render_template('login.html', error=error)
	return render_template('login.html')


@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

@app.route('/register')
def register():
	return render_template('register.html')

class emp_form(Form):
	name = StringField('Name', [validators.DataRequired(), validators.Length(min = 1,max = 50)])
	email = StringField('Email', [validators.DataRequired(),validators.Length(min = 1,max = 50)])
	department = SelectField('Department', choices=[('Overall','Overall'), ('Finance', 'Finance'), ('Research', 'Research'), ('Sales', 'Sales'), ('Marketing', 'Marketing')])
	designation = SelectField('Designation', choices=[('Ceo', 'Ceo'), ('HOD', 'HOD'), ('Manager', 'Manager'), ('Employee', 'Employee'),  ('Intern', 'Intern'),  ('Peon', 'Peon')])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min = 5,max = 50),
		validators.EqualTo('confirm', message="Password do not match")
	])
	confirm = PasswordField('Confirm Password')
	address = StringField('Address', [validators.DataRequired(),validators.Length(min = 1,max = 500)])
	city = StringField('City', [validators.DataRequired(),validators.Length(min = 1,max = 50)])
	state = StringField('State', [validators.DataRequired(),validators.Length(min = 1,max = 50)])
	pincode = StringField('Pin Code', [validators.DataRequired(),validators.Length(min = 1,max = 10)])
	contact = StringField('Contact', [validators.DataRequired(),validators.Length(min = 1,max = 10)])


@app.route('/employee/add', methods=['GET', 'POST'])
@is_admin_logged_in
def add_employee():
	form = emp_form(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		department = form.department.data
		designation = form.designation.data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		pincode = form.pincode.data
		contact = form.contact.data
		password = sha256_crypt.encrypt(str(form.password.data))
		cur = mysql.connection.cursor()
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		cur.execute("INSERT INTO employee(name, email, department, designation, address, contact, password, reg_date, admin, city, state, pincode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s, %s)", (name, email, department, designation, address, contact, password, timestamp, city, state, pincode))
		tm_id = int(cur.lastrowid)
		mysql.connection.commit()
		cur.close()

		flash('Your are now registered with Employee ID : '+str(tm_id) + '. Kindly Note down this ID !!', 'success')
		return redirect(url_for('login'))
	return render_template('add_employee.html', form=form)






if __name__ == '__main__':
	app.secret_key='123456'
	app.run(debug=True)
	 