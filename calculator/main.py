# Flask Imports
from flask import Flask, request, abort, render_template, jsonify, make_response

# Token Imports
import jwt

# System Imports
from datetime import datetime, timedelta

# My imports
import calc_functions as calc_functions
import decorators

def read_number(number_id):
	number = input("Please Enter An Int Number {}: ".format(number_id))

	return int(number)

app = Flask(__name__)

@app.route('/')
def welcome():
	return render_template("index.html")

@app.route('/login', methods=['GET'])
def login_page():
	#run loging attempt
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def attempt_login():
	#run loging attempt
	username = request.form.get('username', type=str)
	password = request.form.get('password', type=str)

	nowTime = str(datetime.now() + timedelta(minutes = 120))

	token = jwt.encode({
		'username': username,
		'expiry': nowTime
	}, 'SECRET_KEY_123456798', algorithm= 'HS256')

	return render_template('login.html', username = username, token = token)

@app.route('/dashboard', methods=['GET'])
@decorators.token_required
def dashboard(username):
	headers = {'Content-Type': 'text/html'}
	return make_response(jsonify(render_template('dashboard.html')), 200, headers)

# URL: 127.0.0.1:5000/add/1/2
@app.route('/op', methods=['POST'])
@decorators.token_required
def perform_operation(username):
	number1 = request.form.get('num1', type=int)
	number2 = request.form.get('num2', type=int)
	op	  = request.form.get('op', type=str)

	if number1 is None or number2 is None or op is None:
		return render_template("dashboard.html", num1 = number1, num2 = number2, op = op)

	if op == '+':
		result = calc_functions.add(number1, number2)
	elif op == '-':
		result = calc_functions.subtract(number1, number2)
	elif op == '*':
		result = calc_functions.multiply(number1, number2)
	elif op == '/':
		result = calc_functions.divide(number1, number2)
	else:
		result = "NULL"

	data = {
		'result': result, 'num1': number1, 'num2': number2, 'op': op
	}

	return make_response(jsonify(data), 200)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', ssl_context = ('certs/pub_cert.pem', 'certs/private_key.pem'))
