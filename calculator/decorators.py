from flask import request, jsonify, make_response, render_template, Blueprint
from functools import wraps

# imports for PyJWT authentication
import jwt

# System Imports
from datetime import datetime, timedelta

# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		print(request.headers)

		if 'Authorization' in request.headers:
			token = request.headers['Authorization']
		elif request.args.get('token', type=str) != "":
			token = request.args.get('token', type=str)
		else:
			token = None

		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			token = token.replace('Bearer ', '', 1)
			print(token)
			data = jwt.decode(token, 'SECRET_KEY_123456798', 'HS256')

			print("----------- decoded data --------")
			print(data)

			expiry_date = datetime.strptime(data['expiry'], '%Y-%m-%d %H:%M:%S.%f')
			if datetime.utcnow() > expiry_date:
				print("Token is expired")

			# check decoded data and find the current_user

		except Exception as e:
			print(e)
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(data['username'], *args, **kwargs)

	return decorated
