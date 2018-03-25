from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static')


# Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'hrmanager'
app.config['MYSQL_CURSORCLASSS'] = 'DictCursor'

#init MYSQL
 
mysql = MySQL(app)


@app.route('/')
def home():
	return render_template('home.html')


@app.route('/employee/view')
def view_employee():
	return render_template('view_employee.html')


@app.route('/attendance')
def attendance():
	return render_template('attendance.html')

@app.route('/incentive')
def incentive():
	return render_template('incentive.html')

@app.route('/salary')
def salary():
	return render_template('salary.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

class emp_form(Form):
	fname = StringField('First Name', [validators.Length(min = 1,max = 50)])
	lname = StringField('Last Name', [validators.Length(min = 1,max = 50)])
	email = StringField('Email', [validators.Length(min = 1,max = 50)])
	department = SelectField('Department', choices=['Overall','Finance','Research','Sales', 'Marketing'])
	designation = SelectField('Designation', choices=['Ceo','HOD','Manager','Employee', 'Intern', 'Peon'])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.Length(min = 5,max = 50),
		validators.EqualTo('confirm', message="Password do not match")
	])
	confirm = PasswordField('Confirm Password')
	address = StringField('Address', [validators.Length(min = 1,max = 500)])


@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
#	print ("Hello")
	form = emp_form(request.form)
	if request.method == 'POST' and form.validate():
		return redirect(url_for('login'))
	return render_template('add_employee.html', form=form)


if __name__ == '__main__':
	app.run(debug=True)
	 