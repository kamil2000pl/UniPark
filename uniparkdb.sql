DROP database IF EXISTS uniparkdb;
CREATE database IF NOT EXISTS uniparkdb;
USE uniparkdb;
DROP TABLE IF EXISTS car_entry, car_exit, transaction_history, payment, car, driver, location, account;

CREATE TABLE account (
	account_id INT AUTO_INCREMENT NOT NULL,
	account_balance DECIMAL(15,2),
	email_address VARCHAR(30),
	password VARCHAR(120),
    PRIMARY KEY (account_id));
    ALTER TABLE account AUTO_INCREMENT=1000;

CREATE TABLE location (
	location_id VARCHAR(8) NOT NULL,
	location_name VARCHAR(30),
	total_spaces INT,
	available_spaces INT,
    PRIMARY KEY (location_id));


CREATE TABLE driver (
	driver_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	college_id VARCHAR(10),
	full_name VARCHAR(30),
    PRIMARY KEY (driver_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id));
    ALTER TABLE driver AUTO_INCREMENT=2000;

CREATE TABLE car (
	registration VARCHAR(15) NOT NULL,
	account_id INT NOT NULL,
    PRIMARY KEY (registration),
    FOREIGN KEY (account_id) REFERENCES account(account_id));

CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT NOT NULL,
	account_id INT NOT NULL,
	name_on_card VARCHAR(30),
	card_number BIGINT,
	card_expiry VARCHAR(5),
	ccv INT,
    PRIMARY KEY (payment_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id));
    ALTER TABLE payment AUTO_INCREMENT=3000;

CREATE TABLE transaction_history (
	transaction_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	date_time TIMESTAMP,
	location_id VARCHAR(8) NOT NULL,
	cost DOUBLE(4,2),
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id));
    ALTER TABLE transaction_history AUTO_INCREMENT=4000;

CREATE TABLE car_entry (
	entry_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	registration VARCHAR(15),
	image VARCHAR(25),
	date_time TIMESTAMP,
    PRIMARY KEY (entry_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id));
    ALTER TABLE car_entry AUTO_INCREMENT=5000;

CREATE TABLE car_exit (
	exit_id INT NOT NULL AUTO_INCREMENT,
	account_id INT NOT NULL,
	registration VARCHAR(15) NOT NULL,
	image VARCHAR(25),
	date_time TIMESTAMP,
    PRIMARY KEY (exit_id),
    FOREIGN KEY (account_id) REFERENCES account(account_id),
    FOREIGN KEY (registration) REFERENCES car(registration));
    ALTER TABLE car_exit AUTO_INCREMENT=6000;


INSERT INTO account VALUES(1000, 0, "d00230552@student.dkit.ie", "sha256$t9IJqsQidBrL50b6$79dbd976e97e250a6847e6cd71fb95fbdf6a5f7833db6cd5ce4e93137c8a65e5");
INSERT INTO account (account_balance, email_address, password) VALUES(5, "d00229452@student.dkit.ie", "sha256$t9IJqsQidBrL50b6$79dbd976e97e250a6847e6cd71fb95fbdf6a5f7833db6cd5ce4e93137c8a65e5");
INSERT INTO account (account_id, account_balance, email_address, password) VALUES(1003, 3.50, "d00197352@student.dkit.ie", "sha256$t9IJqsQidBrL50b6$79dbd976e97e250a6847e6cd71fb95fbdf6a5f7833db6cd5ce4e93137c8a65e5");
INSERT INTO account (account_balance) VALUES(15.00);
INSERT INTO account (account_balance) VALUES(7.50);
INSERT INTO account VALUES(1002, 3.50, "d00230552@student.dkit.ie", "sha256$t9IJqsQidBrL50b6$79dbd976e97e250a6847e6cd71fb95fbdf6a5f7833db6cd5ce4e93137c8a65e5");


INSERT INTO location VALUES
("DKPJF256", "DkIT PJCarrolls Front", 400, 30),
("DKPJB652", "DkIT PJCarrolls Rear", 60, 5);

INSERT INTO driver VALUES
(2000, 1000, "D00230552", "Conor McGuire"),
(2001, 1005, "D00229452", "Kamil Jozefowicz"),
(2002, 1004, "D00197352", "Brian McKenna"),
(2003, 1003, "D00230552", "Jacqueline O'Connor");

INSERT INTO car VALUES
("161LH12345", 1000),
("142LH54321", 1004),
("212LH678", 1003),
("11MH345", 1005),
("10D9393", 1002);

INSERT INTO payment VALUES
(3001, 1000, "Conor McGuire", "1234567812345678", "12/24", "123"),
(3002, 1005, "Kamil Jozefowicz", "8765432187654321", "12/24", "321"),
(3003, 1002, "Brian McKenna", "1234567887654321", "12/24", "312");

INSERT INTO transaction_history VALUES
(4000, 1004, "2021-11-03 23:59:59", "DKPJF256", 10.00),
(4001, 1005, "2021-11-04 23:59:59", "DKPJF256", 5.00),
(4002, 1002, "2021-11-04 23:59:59", "DKPJB652", 2.00);

INSERT INTO car_entry VALUES
(5000, 1000, "161LH12345", "0001.png", "2021-11-03 09:00:00"),
(5001, 1005, "11MH345", "0003.png", "2021-11-03 09:00:00"),
(5002, 1002, "10D9393", "0005.png", "2021-11-04 09:00:00"),
(5003, 1003, "212LH678", "0007.png", "2021-11-04 09:00:00"),
(5004, 1004, "142LH54321", "0008.png", "2021-11-04 17:00:00");

INSERT INTO car_exit VALUES
(6000, 1000, "161LH12345", "0011.png", "2021-11-03 17:00:00"),
(6001, 1005, "11MH345", "0033.png", "2021-11-03 17:00:00"),
(6002, 1002, "10D9393", "0066.png", "2021-11-04 17:00:00");
