DROP database IF EXISTS uniparkdb;
CREATE database IF NOT EXISTS uniparkdb;
USE uniparkdb;
DROP TABLE IF EXISTS entry_exit, transaction_history, payments, cars, users, locations, accounts;

CREATE TABLE accounts (
	account_id INT AUTO_INCREMENT NOT NULL,
	account_balance DOUBLE(4, 2),
PRIMARY KEY (account_id));
ALTER TABLE accounts AUTO_INCREMENT=1000;

CREATE TABLE locations (
	location_id VARCHAR(8) NOT NULL,
	location_name VARCHAR(30),
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
ALTER TABLE users AUTO_INCREMENT=2000;

CREATE TABLE cars (
	registration VARCHAR(15) NOT NULL,
	account_id INT NOT NULL,
PRIMARY KEY (registration),
FOREIGN KEY (account_id) REFERENCES accounts(account_id));

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT NOT NULL,
	account_id INT NOT NULL,
	name_on_card VARCHAR(30),
	card_number BIGINT,
	card_expiry VARCHAR(5),
	ccv INT,
PRIMARY KEY (payment_id),
FOREIGN KEY (account_id) REFERENCES accounts(account_id));
ALTER TABLE payments AUTO_INCREMENT=3000;

CREATE TABLE transaction_history (
	transaction_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	date_time TIMESTAMP,
	location_id VARCHAR(8) NOT NULL,
	cost DOUBLE(4,2),
PRIMARY KEY (transaction_id),
FOREIGN KEY (account_id) REFERENCES accounts(account_id),
FOREIGN KEY (location_id) REFERENCES locations(location_id));
ALTER TABLE transaction_history AUTO_INCREMENT=4000;

-- TODO - decide entry / exit documentation
CREATE TABLE entry_exit (
	entry_exit_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	image_entry VARCHAR(25),
	date_time_entry TIMESTAMP,
	image_exit VARCHAR(25),
	date_time_exit DATETIME,
	registration VARCHAR(15) NOT NULL,
PRIMARY KEY (entry_exit_id),
FOREIGN KEY (account_id) REFERENCES accounts(account_id),
FOREIGN KEY (registration) REFERENCES cars(registration));
ALTER TABLE entry_exit AUTO_INCREMENT=5000;


INSERT INTO accounts VALUES(1000, 0); #--Query can be entered normally without column names
INSERT INTO accounts (account_balance) VALUES(5); #--Using auto increment
INSERT INTO accounts (account_id, account_balance) VALUES(1003, 3.50); #--Query can be entered normally with column names
INSERT INTO accounts (account_balance) VALUES(15.00);
INSERT INTO accounts (account_balance) VALUES(7.50);

INSERT INTO locations VALUES
("DKPJF256", "DkIT PJCarrolls Front", 400, 30),
("DKPJB652", "DkIT PJCarrolls Rear", 60, 5);

INSERT INTO users VALUES
(2000, 1000, "D00230552", "Conor McGuire", "d00230552@student.dkit.ie"),
(2001, 1005, "D00229452", "Kamil Jozefowicz", "d00229452@student.dkit.ie"),
(2002, 1002, "D00197352", "Brian McKenna", "d00197352@student.dkit.ie"),
(2003, 1003, "D00230552", "Jacqueline O'Connor", "d00230552@student.dkit.ie"),
(2004, 1004, "DS04785", "Fred Vradkar", "fvradkar@dkit.ie");

INSERT INTO cars VALUES
("161LH12345", 1000),
("142LH54321", 1004),
("212LH678", 1003),
("11MH345", 1005),
("10D9393", 1002);

INSERT INTO payments VALUES
(3001, 1000, "Conor McGuire", "1234567812345678", "12/24", "123"),
(3002, 1005, "Kamil Jozefowicz", "8765432187654321", "12/24", "321"),
(3003, 1002, "Brian McKenna", "1234567887654321", "12/24", "312");

INSERT INTO transaction_history VALUES
(4000, 1004, "2021-11-03 23:59:59", "DKPJF256", 10.00),
(4001, 1005, "2021-11-04 23:59:59", "DKPJF256", 5.00),
(4002, 1002, "2021-11-04 23:59:59", "DKPJB652", 2.00);

-- TODO - decide entry / exit documentation
INSERT INTO entry_exit VALUES
(5000, 1000, "0001.png", "2021-11-03 09:00:00", "0011.png", "2021-11-03 17:00:00", "161LH12345"),
(5001, 1005, "0003.png", "2021-11-03 09:00:00", "0033.png", "2021-11-03 17:00:00", "11MH345"),
(5004, 1002, "0005.png", "2021-11-04 09:00:00", "0066.png", "2021-11-04 17:00:00", "10D9393"),
(5006, 1003, "0007.png", "2021-11-04 09:00:00", "", "", "212LH678"),
(5007, 1004, "0008.png", "2021-11-04 17:00:00", "", "", "142LH54321");

#--Test Queries
