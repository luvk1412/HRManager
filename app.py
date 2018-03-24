from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/employee')
def employee():
	return render_template('employee.html')

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


if __name__ == '__main__':
	app.run(debug=True)
	 