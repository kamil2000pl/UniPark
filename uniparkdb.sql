DROP database IF EXISTS uniparkdb;
CREATE database IF NOT EXISTS uniparkdb;
USE uniparkdb;
DROP TABLE IF EXISTS entry_exit, transaction_history, payments, cars, users, locations, accounts;

CREATE TABLE accounts (
	account_id INT AUTO_INCREMENT NOT NULL,
	account_balance DOUBLE(4, 2),
	PRIMARY KEY (account_id));
	
CREATE TABLE locations (
	location_id INT NOT NULL,
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
	card_number INT,
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
	FOREIGN KEY (account_id) REFERENCES accounts(account_id));

