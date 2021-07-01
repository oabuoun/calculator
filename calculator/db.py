from mysql.connector import connect, Error

DB_SERVER = "mysql_dbms"
DB_USER = "root"
DB_PASSWORD = "my_secret_password"
DB_NAME = "calc_log_db"

def log(operation, num1, num2, result):
    with connect(host=DB_SERVER, user=DB_USER, password=DB_PASSWORD , database=DB_NAME) as connection:
        with connection.cursor()as cursor:
            command = "INSERT INTO `requests` (`operation`, `num1`, `num2`, `result`) VALUES ('{}',{}, {}, {});".format(operation, num1, num2, result)
            cursor.execute(command)
            connection.commit()
