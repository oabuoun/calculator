from flask import Flask, request, abort, render_template
import calc_functions as calc_functions
import db

def read_number(number_id):
    number = input("Please Enter An Int Number {}: ".format(number_id))

    return int(number)

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html")


# URL: 127.0.0.1:5000/add/1/2
@app.route('/add/<int:number1>/<int:number2>')
def perform_add(number1, number2):
    number3 = calc_functions.add(number1, number2)
    return str(number3)


# URL: 127.0.0.1:5000/add/1/2
@app.route('/operation', methods=['GET', 'POST'])
def perform_operation():
    number1 = request.form.get('num1', type=int)
    number2 = request.form.get('num2', type=int)
    op      = request.form.get('op', type=str)
    if number1 is None or number2 is None:
        abort(400)

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

    return render_template("result.html", result = result, num1 = number1, num2 = number2, op = op)

# Using Query String
# URL: 127.0.0.1:5000/add?num1=1&num2=2
@app.route('/add')
def perform_add_query():
    number1 = request.args.get('num1', type=int)
    number2 = request.args.get('num2', type=int)

    if number1 is None or number2 is None:
        abort(400)

    result = calc_functions.add(number1, number2)
    db.log("add", number1, number2, result)

    return str(result)

@app.route('/subtract')
def perform_subtract_query():
    number1 = request.args.get('num1', type=int)
    number2 = request.args.get('num2', type=int)

    if number1 is None or number2 is None:
        abort(404)

    number3 = calc_functions.subtract(number1, number2)
    return str(number3)


@app.route('/multiply')
def perform_multiply_query():
    number1 = request.args.get('num1', type=int)
    number2 = request.args.get('num2', type=int)

    if number1 is None or number2 is None:
        abort(404)

    number3 = calc_functions.multiply(number1, number2)
    return str(number3)


@app.route('/divide')
def perform_divide_query():
    number1 = request.args.get('num1', type=int)
    number2 = request.args.get('num2', type=int)

    if number1 is None or number2 is None:
        abort(404)

    number3 = calc_functions.divide(number1, number2)
    return str(number3)

if __name__ == '__main__':
    #number1 = read_number(1)
    #number2 = read_number(2)

    #result = calc_functions.add(number1, number2)
    #print(result)
    app.run(debug=True, host='0.0.0.0')
