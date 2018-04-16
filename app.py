from flask import Flask, render_template, flash, redirect, request, url_for, session, logging, jsonify, make_response
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField,FileField
from flask_wtf.file import FileField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mysqldb import MySQL
import datetime, time
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import pdfkit
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


# Checking autharised acces for non admin lgoin
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unautharized, Please Login', 'danger')
			return redirect(url_for('login'))
	return wrap


#cehcking autharised access for admin login
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





# Dashboard

@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
	if request.method == 'POST':
		emp_id = session['emp_id']
		cur = mysql.connection.cursor()
		if request.form['btn'] == 'attendance':
			from_date = request.form['from']
			to_date = request.form['to']
			if to_date < from_date:
				error='To Date cannot be smaller than From date'
				return render_template('dashboard.html', error=error)
			att_ct = cur.execute("SELECT * FROM attendance WHERE id = %s && date >= %s && date <= %s", (emp_id, from_date, to_date))
			msg='Your attendance from ' + from_date + ' to ' + to_date + ' is ' + str(att_ct) + ' days !!'
			cur.close()
			flash(msg, 'info')
			return render_template('dashboard.html')
		elif request.form['btn'] == 'incentive':
			from_date = request.form['fromm']
			to_date = request.form['too']
			if to_date < from_date:
				error='To Date cannot be smaller than From date'
				return render_template('dashboard.html', error=error)
			app.logger.info(from_date)
			app.logger.info(to_date)
			tmp2 = cur.execute("SELECT * FROM incentive WHERE id = %s && date >= %s && date <= %s", (emp_id, from_date, to_date))
			incent_tot = 0
			for _ in range(tmp2):
				tmp_data = cur.fetchone()
				incent_tot += tmp_data['hours']
			msg='Your incentive from ' + from_date + ' to ' + to_date + ' is ' + str(incent_tot) + ' hours !!'
			cur.close()
		#	flash(msg, 'info')
			return render_template('dashboard.html', msg=msg)
	return render_template('dashboard.html')


# Employee View

@app.route('/employee/view', methods=['GET', 'POST'])
@is_admin_logged_in
def view_employee():
	cur_ = mysql.connection.cursor()
	res = cur_.execute("SELECT * FROM salary")
	depts = []
	desigs = []
	for _ in range(res):
		tmp = cur_.fetchone()
		if tmp['department'] not in depts:
			depts.append(tmp['department'])
		if tmp['designation'] not in desigs:
			desigs.append(tmp['designation'])
	if request.method == 'POST':
		inst = ""
		flag = 0
		if request.form.get('cdepartment'):
			if flag == 0:
				inst += " WHERE department='"+request.form['department']+"'"
				flag = 1
			else:
				inst += " && department='"+request.form['department']+"'"

		if request.form.get('cdesignation'):
			if flag == 0:
				inst += " WHERE designation='"+request.form['designation']+"'"
				flag = 1
			else:
				inst += " && designation='"+request.form['designation']+"'"
		if request.form.get('cage'):
			age=request.form['age']
			#finding cur date
			ts = time.time()
			tmp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			####
			date = str(int(tmp[:-6]) - int(age)) + tmp[4:]
			if flag == 0:

				inst += " WHERE dob>='"+date+"'"
				flag = 1
			else:
				inst += " && dob>='"+date+"'"
		if request.form.get('cgender'):
			if flag == 0:
				inst += " WHERE gender='"+request.form['gender']+"'"
				flag = 1
			else:
				inst += " && gender='"+request.form['gender']+"'"

		if request.form.get('ccity'):
			if flag == 0:
				inst += " WHERE city='"+request.form['city']+"'"
				flag = 1
			else:
				inst += " && city='"+request.form['city']+"'"
		if request.form.get('cstate'):
			if flag == 0:
				inst += " WHERE state='"+request.form['state']+"'"
				flag = 1
			else:
				inst += " && state='"+request.form['state']+"'"
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM e_v"+inst)
		if result > 0:
			employees = cur.fetchall()
			cur.close()
			return render_template('view_employee.html', employees=employees,depts = depts, desigs = desigs)
		else:
			msg='No Employee Found'
			cur.close()
			return render_template('view_employee.html', error=msg,depts = depts, desigs = desigs)
	return render_template('view_employee.html', depts = depts, desigs = desigs)


# Attendance

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


# Incentive

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


# calculate salary

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
		result = cur.execute("SELECT * FROM e_v WHERE id = %s", [emp_id])
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
			salary_tot = 0
			salary_tot += salary_data['amount_per_hour'] * (att_ct + incent_tot)
			if request.form['btn'] == 'cal':
				msg='Salary for the employee with id ' + str(emp_data['id']) + ' from ' + from_date + ' to ' + to_date + ' is ' + str(salary_tot)
				cur.close()
				flash(msg, 'info')
				return render_template('salary.html')
			elif request.form['btn'] == 'gen':
				rendered = render_template('payroll.html', employee=emp_data, fro=from_date,to=to_date,salary=salary_tot)
				pdf = pdfkit.from_string(rendered, False)
				response = make_response(pdf)
				response.headers['Content-Type'] = 'application/pdf'
				response.headers['Content-Disposition'] = 'inline; filename=payroll.pdf'
				return response
		else:
			error='Employee id not found'
			cur.close()
			return render_template('salary.html', error=error)
	return render_template('salary.html')




#About page

@app.route('/about')
def about():
	return render_template('about.html')


#profile page

@app.route('/profile/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def profile(id):
	#emp_id = session['emp_id']
	emp_id = id
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM e_v WHERE id = %s", [emp_id])
	if result > 0:
		employee = cur.fetchone()
		employee['id'] = str(employee['id'])
		cur.close()
		return render_template('profile.html', employee=employee)
	error='Employee Not found'
	return render_template('profile.html', error=error)


#edit profile profile

class edit_form(Form):
	name = StringField('Name', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	gender=SelectField('Gender', choices=[('male','male'), ('female','female'), ('other', 'other')],render_kw={"required": ""})
	email = StringField('Email', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})

	address = StringField('Address', [validators.DataRequired(),validators.Length(min = 1,max = 500)],render_kw={"required": ""})
	city = StringField('City', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	state = StringField('State', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	nationality = StringField('Nationality', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})

	pincode = StringField('Pin Code', [validators.DataRequired(),validators.Length(min = 1,max = 10)],render_kw={"required": ""})
	contact = StringField('Contact', [validators.DataRequired(),validators.Length(min = 1,max = 10)],render_kw={"required": ""})


@app.route('/edit_profile/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_profile(id):
	#emp_id = session['emp_id']
	emp_id = id;
	form = edit_form(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		gender = form.gender.data
		dob = request.form['dob']
		email = form.email.data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		nationality = form.nationality.data
		pincode = form.pincode.data
		contact = form.contact.data

		cur = mysql.connection.cursor()
		#finding cur date
		# ts = time.time()
		# timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		####
		# cur.execute("INSERT INTO employee(name, email, department, designation, address, contact, password, reg_date, admin, pincode, gender, dob) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s, %s)", (name, email, department, designation, address, contact, password, timestamp, pincode, gender, dob))
		cur.execute("UPDATE employee SET name=%s, email=%s, contact=%s, address=%s, dob=%s, pincode=%s ,gender=%s WHERE id=%s", (name, email, contact, address, dob, pincode, gender, id))
		tm_id = int(cur.lastrowid)
		result = cur.execute("SELECT * FROM city_state WHERE pincode=%s",[pincode]);
		if result==0:
			cur.execute("INSERT INTO city_state(city,state,pincode) VALUES (%s,%s,%s)", (city,state,pincode))
		result = cur.execute("SELECT * FROM state_nationality WHERE state=%s",[state]);
		if result==0:
			cur.execute("INSERT INTO state_nationality(state,nationality) VALUES (%s,%s)", (state, nationality))
		mysql.connection.commit()
		cur.close()
		img_new_name = str(tm_id)
		flag = 0


		if 'profile_image' in request.files:
			file = request.files['profile_image']
			file.filename = str(tm_id) + '.jpg'
			photos.save(file)
		flash('Employee details updated', 'success')
		return redirect('/profile/'+emp_id)

	emp_id = id
	cur = mysql.connection.cursor()
	result = cur.execute("SELECT * FROM e_v WHERE id = %s", [emp_id])
	if result > 0:
		employee = cur.fetchone()
		employee['id'] = str(employee['id'])
		cur.close()
		return render_template('edit_profile.html', form=form , employee=employee)
	return render_template('edit_profile.html', form=form , employee=employee)


#login page

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


# logout

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))


class check_password(Form):
	old_password = PasswordField('Old Password', [
			validators.DataRequired(),
			validators.Length(min = 5,max = 50)
		],render_kw={"required": ""})
	new_password = PasswordField('New Password', [
		validators.DataRequired(),
		validators.Length(min = 5,max = 50),
		validators.EqualTo('confirm_newpassword', message="Password do not match")
	],render_kw={"required": ""})
	confirm_newpassword = PasswordField('Confirm Password',render_kw={"required": ""})

@app.route('/change_password', methods=['GET','POST'])
@is_logged_in
def change_password():
	form = check_password(request.form)
	if request.method == 'POST'and form.validate():
		emp_id = session['emp_id']
		old_password = form.old_password.data
		new_password = sha256_crypt.encrypt(str(form.new_password.data))

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			data = cur.fetchone()
			password = data['password']
			if sha256_crypt.verify(old_password, password):
				error='Password Match'
				result2 = cur.execute("UPDATE employee SET password = %s WHERE id = %s", (new_password, emp_id))
				mysql.connection.commit()
				cur.close()
				error = "Password Changed Successfully"
				flash(error, 'success')
				return redirect('/profile/'+str(emp_id))
			else:
				error='Password does not match, If you don\'t remember Click Forgot Password'
				cur.close()
				return render_template('change_password.html', form = form, error=error)
		else:
			error='Employee id not found'
			cur.close()
			return render_template('change_password.html', form = form, error=error)
	return render_template('change_password.html', form = form)



@app.route('/register')
def register():
	return render_template('register.html')



# Add employee
			# Employee form
class emp_form(Form):
	name = StringField('Name', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	gender=SelectField('Gender', choices=[('',''),('male','male'), ('female','female'), ('other', 'other')],render_kw={"required": ""})
	email = StringField('Email', [validators.DataRequired(),validators.Length(min = 1,max = 50), validators.Email()],render_kw={"required": ""})
	# cur = mysql.connection.cursor()
	# result = cur.execute("SELECT department FROM salary");
	department = SelectField('Department', choices=[('','')],render_kw={"required": ""})
	designation = SelectField('Designation', choices=[('','')],render_kw={"required": ""})
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min = 5,max = 50),
		validators.EqualTo('confirm', message="Password do not match")
	],render_kw={"required": ""})
	confirm = PasswordField('Confirm Password',render_kw={"required": ""})
	address = StringField('Address', [validators.DataRequired(),validators.Length(min = 1,max = 500)],render_kw={"required": ""})
	city = StringField('City', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	state = StringField('State', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	nationality = StringField('Nationality', [validators.DataRequired(),validators.Length(min = 1,max = 50)],render_kw={"required": ""})

	pincode = StringField('Pin Code', [validators.DataRequired(),validators.Length(min = 1,max = 10)],render_kw={"required": ""})
	contact = StringField('Contact', [validators.DataRequired(),validators.Length(min = 1,max = 10)],render_kw={"required": ""})





#Addtion
@app.route('/employee/add', methods=['GET', 'POST'])
@is_admin_logged_in
def add_employee():
	form = emp_form(request.form)
	cur_ = mysql.connection.cursor()
	res = cur_.execute("SELECT * FROM salary")
	depts = []
	desigs = []
	form.department.choices = [('','')]
	form.designation.choices = [('','')]
	for _ in range(res):
		tmp = cur_.fetchone()
		if tmp['department'] not in depts:
			depts.append(tmp['department'])
		if tmp['designation'] not in desigs:
			desigs.append(tmp['designation'])
	for i in depts:
		form.department.choices += [(i,i)]
	for i in desigs:
		form.designation.choices += [(i,i)]
	cur_.close()
	if request.method == 'POST' and form.validate():
		name = form.name.data
		gender = form.gender.data
		dob = request.form['dob']
	#	dob="2017-12-14"
	#	app.logger.info(dob)
		email = form.email.data
		department = form.department.data
		designation = form.designation.data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		nationality = form.nationality.data
		pincode = form.pincode.data
		contact = form.contact.data
		password = sha256_crypt.encrypt(str(form.password.data))
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT designation FROM salary where department=%s",[department])
		tmp = []
		for _ in range(result):
			data = cur.fetchone()
			tmp.append(data['designation'])
		if designation not in tmp:
			error='The following combination of department and designation is not available'
			return render_template('add_employee.html', form=form, error=error)
		#finding cur date
		ts = time.time()
		timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		####
		cur.execute("INSERT INTO employee(name, email, department, designation, address, contact, password, reg_date, admin, pincode, gender, dob) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s, %s)", (name, email, department, designation, address, contact, password, timestamp, pincode, gender, dob))
		tm_id = int(cur.lastrowid)
		result = cur.execute("SELECT * FROM city_state WHERE pincode=%s",[pincode]);
		if result==0:
			cur.execute("INSERT INTO city_state(city,state,pincode) VALUES (%s,%s,%s)", (city,state,pincode))
		result = cur.execute("SELECT * FROM state_nationality WHERE state=%s",[state]);
		if result==0:
			cur.execute("INSERT INTO state_nationality(state,nationality) VALUES (%s,%s)", (state, nationality))
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




class change_dep(Form):
	emp_id = StringField('Employee ID', [validators.DataRequired()], render_kw={"required": ""} )
	department = SelectField('Department', choices=[('','')],render_kw={"required": ""})
	designation = SelectField('Designation', choices=[('','')],render_kw={"required": ""})


@app.route('/employee/change_department', methods=['GET', 'POST'])
@is_admin_logged_in
def change_department():
	form = change_dep(request.form)
	cur_ = mysql.connection.cursor()
	res = cur_.execute("SELECT * FROM salary")
	depts = []
	desigs = []
	form.department.choices = [('','')]
	form.designation.choices = [('','')]
	for _ in range(res):
		tmp = cur_.fetchone()
		if tmp['department'] not in depts:
			depts.append(tmp['department'])
		if tmp['designation'] not in desigs:
			desigs.append(tmp['designation'])
	for i in depts:
		form.department.choices += [(i,i)]
	for i in desigs:
		form.designation.choices += [(i,i)]
	cur_.close()

	if request.method == 'POST'and form.validate():
		emp_id = form.emp_id.data
		department = form.department.data
		designation = form.designation.data

		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM employee WHERE id = %s", [emp_id])
		if result > 0:
			cur.execute("UPDATE employee SET designation = %s, department = %s WHERE id=%s",(designation, department, emp_id))

			mysql.connection.commit()
			cur.close()
			return render_template('change_department.html', form = form)
		else:
			error='Employee id not found'
			cur.close()
			return render_template('change_department.html', form = form, error=error)

	return render_template('change_department.html', form = form)


class add_dep(Form):
	department = StringField('Department', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	designation = StringField('Designation', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	salary = StringField('Salary', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
class add_des(Form):
	department = SelectField('Department', choices=[('','')],render_kw={"required": ""})
	designation = StringField('Designation', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})
	salary = StringField('Salary', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})

class upd_sal(Form):
	department = SelectField('Department', choices=[('','')],render_kw={"required": ""})
	designation = SelectField('Designation', choices=[('','')],render_kw={"required": ""})
	salary = StringField('Salary', [validators.DataRequired(), validators.Length(min = 1,max = 50)],render_kw={"required": ""})


@app.route('/hierarchy', methods=['GET', 'POST'])
@is_logged_in
def hierarchy():
	form1 = add_dep(request.form)
	form2 = add_des(request.form)
	form3 = upd_sal(request.form)
	cur_ = mysql.connection.cursor()
	res = cur_.execute("SELECT * FROM salary")
	depts = []
	desigs = []
	form2.department.choices = [('','')]
	form3.department.choices = [('','')]
	form3.designation.choices = [('','')]
	for _ in range(res):
		tmp = cur_.fetchone()
		if tmp['department'] not in depts:
			depts.append(tmp['department'])
		if tmp['designation'] not in desigs:
			desigs.append(tmp['designation'])
	for i in depts:
		form2.department.choices += [(i,i)]
		form3.department.choices += [(i,i)]
	for i in desigs:
		form3.designation.choices += [(i,i)]
	if request.method == 'POST':
		if request.form['btn'] == 'form1' and form1.validate():
			print("11")
			department = form1.department.data
			designation = form1.designation.data
			salary = form1.salary.data
			salary = int(salary)
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO salary(department,designation,amount_per_hour) VALUES(%s, %s, %s)", (department, designation, salary))
			cur.connection.commit()
			cur.close()
			flash('Data added', 'success')
		if request.form['btn'] == 'form2' and form2.validate():
			print("22")
			department = form2.department.data
			designation = form2.designation.data
			salary = form2.salary.data
			salary = int(salary)
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO salary(department,designation,amount_per_hour) VALUES(%s, %s, %s)", (department, designation, salary))
			cur.connection.commit()
			cur.close()
			flash('Designation and Salary added', 'success')
		if request.form['btn'] == 'form3' and form3.validate():
			print("33")
			department = form3.department.data
			designation = form3.designation.data
			salary = form3.salary.data
			salary = int(salary)
			cur = mysql.connection.cursor()
			result = cur.execute("SELECT designation FROM salary where department=%s",[department])
			tmp = []
			for _ in range(result):
				data = cur.fetchone()
				tmp.append(data['designation'])
			if designation not in tmp:
				error='The following combination of department and designation is not available'
				return render_template('hierarchy.html', form1 = form1, form2 = form2, form3=form3, error=error)
			cur.execute("UPDATE salary SET amount_per_hour=%s WHERE department=%s AND designation= %s", (salary, department, designation))
			cur.connection.commit()
			cur.close()
			flash('Salary Updated', 'success')
		return redirect(url_for('hierarchy'))
	return render_template('hierarchy.html', form1 = form1, form2 = form2, form3=form3)


@app.route('/make_admin/<string:id>', methods=['GET', 'POST'])
@is_admin_logged_in
def make_admin(id):
	cur = mysql.connection.cursor()
	id = int(id)
	cur.execute("UPDATE employee SET admin=1 WHERE id=%s", [id])
	mysql.connection.commit()
	cur.close()
	return jsonify("done"), 200

@app.route('/remove_admin/<string:id>', methods=['GET', 'POST'])
@is_admin_logged_in
def remove_admin(id):
	cur = mysql.connection.cursor()
	id = int(id)
	if id == 1:
		return jsonify("cannot remove from admin"), 400

	cur.execute("UPDATE employee SET admin=0 WHERE id=%s", [id])
	mysql.connection.commit()
	cur.close()
	return jsonify("done"), 200


#Delete employee
@app.route('/delete/<string:id>', methods=['GET', 'POST'])
@is_admin_logged_in
def del_emp(id):
	emp_id = id
	id=int(id)
	if id == 1:
		return jsonify("cannot remove"), 400
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM employee WHERE id = %s", [emp_id])
	mysql.connection.commit()
	cur.close()
	return jsonify("done"), 200


@app.route('/')
def index():
	if session['logged_in']:
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('login'))
# from flask import Response

# @app.route("/")
# def hello():
#     return '''
#         <html><body>
#         Hello. <a href="/getPlotCSV" class="btn btn-primary">Click me.</a>
#         </body></html>
#         '''

# @app.route("/getPlotCSV")
# def getPlotCSV():
#     # with open("outputs/Adjacency.csv") as fp:
#     #     csv = fp.read()
#     csv = '1,2,3\n4,5,6\n'
#     return Response(
#         csv,
#         mimetype="text/csv",
#         headers={"Content-disposition":
#                  "attachment; filename=myplot.csv"})

# # Main


if __name__ == '__main__':
	app.secret_key='123456'
	app.run(debug=True)
