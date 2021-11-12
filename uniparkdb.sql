DROP database IF EXISTS uniparkdb;
CREATE database IF NOT EXISTS uniparkdb;
USE uniparkdb;
DROP TABLE IF EXISTS entry_exit, transaction_history, payments, cars, users, locations, accounts;

CREATE TABLE accounts (
	account_id INT AUTO_INCREMENT NOT NULL,
	account_balance DOUBLE(4, 2),
	PRIMARY KEY (account_id));
	
CREATE TABLE locations (
	location_id INT NOT NULL AUTO_INCREMENT,
	location_name VARCHAR(20),
	total_spaces INT,
	available_spaces INT,
	PRIMARY KEY (location_id));
	
CREATE TABLE users (
	user_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	college_id VARCHAR(10),
	full_name VARCHAR(30),
	email_address VARCHAR(30),
	PRIMARY KEY (user_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id));
	
CREATE TABLE cars (
	registration VARCHAR(15) NOT NULL,
	account_id INT NOT NULL,
	make VARCHAR(15),
	model VARCHAR(15),
	colour VARCHAR(10),
	PRIMARY KEY (registration),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id));
	
CREATE TABLE payments (
	account_id INT NOT NULL,
	card_number BIGINT,
	card_expiry VARCHAR(5),
	ccv INT,
	PRIMARY KEY (card_number),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id));

CREATE TABLE transaction_history (
	transaction_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	date_time TIMESTAMP,
	location_id INT NOT NULL,
	cost DOUBLE(4,2),
	PRIMARY KEY (transaction_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id),
	FOREIGN KEY (location_id) REFERENCES locations(location_id));
	
CREATE TABLE entry_exit (
	entry_exit_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	date_time TIMESTAMP,
	registration VARCHAR(15) NOT NULL,
	registration_image VARCHAR(25),
	PRIMARY KEY (entry_exit_id),
	FOREIGN KEY (account_id) REFERENCES accounts(account_id),
	FOREIGN KEY (registration) REFERENCES cars(registration));
	
	

INSERT INTO accounts VALUES(1, 0); #--Query can be entered normally without column names
INSERT INTO accounts (account_balance) VALUES(5); #--Using auto increment
INSERT INTO accounts (account_id, account_balance) VALUES(3, 3.50); #--Query can be entered normally with column names

INSERT INTO locations VALUES(1, "DkIT PJCarrolls", 400, 30);
INSERT INTO locations (location_name, total_spaces, available_spaces) VALUES("DkIT PJCarrolls Rear", 60, 5); #--Using auto increment

INSERT INTO users VALUES(1, 1, "D00230552", "Conor McGuire", "d00230552@student.dkit.ie");
INSERT INTO users VALUES(2, 1, "d00229452", "Kamil Jozefowicz", "d00229452@student.dkit.ie");
INSERT INTO users VALUES(3, 2, "d00197352", "Brian McKenna", "d00197352@student.dkit.ie");
INSERT INTO users (account_id, college_id, full_name, email_address) VALUES(2, "DkIT", "Jacqueline O'Connor", "d00230552@student.dkit.ie");
INSERT INTO users (account_id, college_id, full_name, email_address) VALUES(3, "DkIT", "Fred Vradkar", "fvradkar@dkit.ie");

INSERT INTO cars VALUES("161LH12345", 1, "Nissan", "Micra", "Silver");
INSERT INTO cars VALUES("142LH54321", 1, "Skoda", "Octavia", "Red");
INSERT INTO cars VALUES("212LH678", 2, "Audi", "A6", "Black");
INSERT INTO cars VALUES("11MH345", 2, "Toyota", "Corolla", "Blue");
INSERT INTO cars VALUES("10D9393", 3, "Ford", "Focus", "Grey");
INSERT INTO cars VALUES("05C2929", 3, "Honda", "Civic", "Silver");

INSERT INTO payments VALUES(1, "1234567812345678", "12/24", "123");
INSERT INTO payments VALUES(2, "8765432187654321", "12/24", "321");
INSERT INTO payments VALUES(3, "1234567887654321", "12/24", "312");

INSERT INTO transaction_history VALUES(1, 1, "2021-11-03 23:59:59", 1, 4.00);
INSERT INTO transaction_history VALUES(2, 2, "2021-11-04 23:59:59", 2, 2.00);
INSERT INTO transaction_history VALUES(3, 3, "2021-11-04 23:59:59", 1, 2.00);

INSERT INTO entry_exit VALUES(1, 1, "2021-11-03 09:00:00", "161LH12345", "0001.png");
INSERT INTO entry_exit VALUES(2, 1, "2021-11-03 09:00:00", "142LH54321", "0002.png");
INSERT INTO entry_exit VALUES(3, 1, "2021-11-03 17:00:00", "161LH12345", "0003.png");
INSERT INTO entry_exit VALUES(4, 1, "2021-11-03 17:00:00", "142LH54321", "0004.png");


INSERT INTO entry_exit VALUES(5, 2, "2021-11-04 09:00:00", "212LH678", "0005.png");
INSERT INTO entry_exit VALUES(6, 2, "2021-11-04 17:00:00", "212LH678", "0006.png");

INSERT INTO entry_exit VALUES(7, 3, "2021-11-04 09:00:00", "10D9393", "0007.png");
INSERT INTO entry_exit VALUES(8, 3, "2021-11-04 17:00:00", "05C2929", "0008.png");

#--Test Queries

#--User Registration
INSERT INTO accounts (account_balance) VALUES(0); 
INSERT INTO users (account_id, college_id, full_name, email_address) VALUES(3, "DkIT", "Fred Vradkar", "fvradkar@dkit.ie");

#--User Login
SELECT *
FROM users JOIN accounts USING (account_id)
WHERE users(email_address)

#--Add car
SELECT 
INSERT INTO cars VALUES("161LH12345", 1, "Nissan", "Micra", "Silver");

#--Add User
INSERT INTO users (account_id, college_id, full_name, email_address) VALUES(3, "DkIT", "Fred Vradkar", "fvradkar@dkit.ie");

#--Edit User

#--Edit Car

#--Edit Payment

#--Check transaction history (user)

#--Check entry exit (user)

#--Car enters (Reg)

#--Car enters(Student id)

#--Car enters (Ticket)

#--Car Exits (Student id)

#--Car Exits (Ticket)

#--Car Exits  (Reg)

#--Delete Account

#-- Delete User
