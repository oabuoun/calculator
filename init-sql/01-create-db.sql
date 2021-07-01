CREATE DATABASE calc_log_db;
USE calc_log_db;
CREATE TABLE requests (requestid INT NOT NULL AUTO_INCREMENT, operation VARCHAR(10), num1 FLOAT, num2 FLOAT, result FLOAT, PRIMARY KEY (requestid));
