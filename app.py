from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField,FileField
from flask_wtf.file import FileField
from passlib.hash import sha256_crypt
from functools import wraps 
from flask_mysqldb import MySQL
import datetime, time
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
app = Flask(__name__, static_url_path='/static')


# Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'hrmanager'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
 
mysql = MySQL(app)

#Uploads

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)




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

@app.route('/attendance', methods=['GET', 'POST'])
@is_admin_logged_in
def attendance():
	if request.method == 'POST':
		emp_id = request.form['emp_id']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			#finding cur date
			ts = time.time()
			timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			####
			result2 = cur.execute("SELECT * FROM attendance WHERE date = %s", [timestamp])
			flag = 0
			for i in range(result2):
				data = cur.fetchone()
				if data['id'] == int(emp_id):
					flag = 1
					break
			if flag == 1:		
				error='Today\'s attendance is already marked for this employee'
				cur.close()
				return render_template('attendance.html', error=error)
			else:
				cur.execute("INSERT INTO attendance(date, id) VALUES(%s, %s)", (timestamp, emp_id))
				mysql.connection.commit()
				error='Attendance marked succesfully for employee with Employee id ' + str(emp_id)
				cur.close()
				return render_template('attendance.html', msg=error)
		else:
			error='Employee id not found'
			cur.close()
			return render_template('attendance.html', error=error)
	return render_template('attendance.html')

@app.route('/incentive', methods=['GET','POST'])
@is_admin_logged_in
def incentive():
	if request.method == 'POST':
		emp_id = request.form['emp_id']
		hours = request.form['hours']
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			#finding cur date
			ts = time.time()
			timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			####
			result2 = cur.execute("SELECT * FROM incentive WHERE date = %s", [timestamp])
			flag = 0
			for _ in range(result2):
				data = cur.fetchone()
				if data['id'] == int(emp_id):
					flag = 1
					break
			if flag == 1:		
				error='Today\'s incentive is already added for this employee'
				cur.close()
				return render_template('incentive.html', error=error)
			else:
				cur.execute("INSERT INTO incentive(date, hours, id) VALUES(%s, %s, %s)", (timestamp, hours, emp_id))
				mysql.connection.commit()
				error='Attendance marked succesfully for employee with Employee id ' + str(emp_id)
				cur.close()
				return render_template('incentive.html', msg=error)
		else:
			error='Employee id not found'
			cur.close()
			return render_template('incentive.html', error=error)
	return render_template('incentive.html')


@app.route('/salary', methods=['GET', 'POST'])
@is_admin_logged_in
def salary():
	if request.method == 'POST':
		emp_id = request.form['emp_id']
		from_date = request.form['from']
		to_date = request.form['to']
		if to_date < from_date:
			error='To Date cannot be smaller than From date'
			return render_template('salary.html', error=error)
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			emp_data = cur.fetchone()
			tmp = cur.execute("SELECT * FROM salary WHERE department = %s && designation = %s", (emp_data['department'], emp_data['designation']))
			salary_data = cur.fetchone()
			att_ct = cur.execute("SELECT * FROM attendance WHERE id = %s && date >= %s && date <= %s", (emp_id, from_date, to_date))
			att_ct *= 10
			tmp2 = cur.execute("SELECT * FROM incentive WHERE id = %s && date >= %s && date <= %s", (emp_id, from_date, to_date))
			incent_tot = 0
			for _ in range(tmp2):
				tmp_data = cur.fetchone()
				incent_tot += tmp_data['hours']
			app.logger.info(att_ct)
			app.logger.info(incent_tot)
			app.logger.info(salary_data['amount_per_hour'])
			salary_tot = 0
			salary_tot += salary_data['amount_per_hour'] * (att_ct + incent_tot)
			msg='Salary for the employee with id ' + str(emp_data['id']) + ' from ' + from_date + ' to ' + to_date + ' is ' + str(salary_tot)  
			cur.close()
			flash(msg, 'success')
			return render_template('salary.html')		
		else:
			error='Employee id not found'
			cur.close()
			return render_template('salary.html', error=error)
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
				if data['admin'] == 1:
					session['admin_logged_in'] = True
					flash('You are now loged in as an Admin', 'success')
				else:
					flash('You are now loged in as an employee', 'success')
				cur.close()
				return redirect(url_for('dashboard'))
			else:
				error='Password does not match, If you don\'t remember Click Forgot Password'
				cur.close()
				return render_template('login.html', error=error)
		else:
			error='Employee id not found'
			cur.close()
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
	gender=SelectField('Gender', choices=[('male','male'), ('female','female'), ('other', 'other')])
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
		gender = form.gender.data
		email = form.email.data
		department = form.department.data
		designation = form.designation.data
		if department == 'Overall' and (designation != 'Peon' or designation != 'Ceo'):
			error='Overall can be Ceo or Peon'
			return render_template('add_employee.html', form=form, error=error)
		if department != 'Overall' and (designation == 'Peon' or designation == 'Ceo'):
			error='Ceo or Peon can only be overall'
			return render_template('add_employee.html', form=form, error=error)
		address = form.address.data
		city = form.city.data
		state = form.state.data
		pincode = form.pincode.data
		contact = form.contact.data
		password = sha256_crypt.encrypt(str(form.password.data))
		cur = mysql.connection.cursor()
		#finding cur date
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		####
		cur.execute("INSERT INTO employee(name, email, department, designation, address, contact, password, reg_date, admin, city, state, pincode, gender) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s, %s, %s)", (name, email, department, designation, address, contact, password, timestamp, city, state, pincode, gender))
		tm_id = int(cur.lastrowid)
		mysql.connection.commit()
		cur.close()
		img_new_name = str(tm_id)
		flag = 0
		if 'profile_image' in request.files:
			file = request.files['profile_image']
			file.filename = str(tm_id) + '.jpg'
			photos.save(file)
		flash('Employee has been added with Employee ID : '+str(tm_id) + '. Kindly Note down this ID !!', 'success')
		return redirect(url_for('add_employee'))
	return render_template('add_employee.html', form=form)






if __name__ == '__main__':
	app.secret_key='123456'
	app.run(debug=True)
	 