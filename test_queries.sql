#--Test Queries

#--User Registration
#--When a user registers they enter full name, email and password
    #--check email has not already been used for an account
    SELECT COUNT(email_address) FROM accounts WHERE email_address = "steadyfreddy@gmail.com";
    #--insert new user details
    INSERT INTO accounts (account_balance, email_address, password) VALUES(0, "steadyfreddy@gmail.com", "password2");
    INSERT INTO users (account_id, full_name) VALUES (1007, "Fred Vradkar");

#--User Login
#--User enters their email and password, if they match account id is returned, otherwise return -1
    SELECT password FROM account WHERE email_address = "steadyfreddy@gmail.com"
    #--returns password hash, check it in python
    #--If password matches
    SELECT account_id, full_name FROM accounts WHERE email_address = "steadyfreddy@gmail.com" AND password = "password2"
    #--If it doesnt match, return string

#--Add car
    #--Make sure that no more than 3 cars per account
    SELECT COUNT(registration) FROM cars WHERE account_id = 1;
    #--Make sure car is not already in db
    SELECT COUNT(registration) FROM cars WHERE registration = "06LH11544";
    #--Insert query
    INSERT INTO cars VALUES ("06LH11544", 100);

#--Add User

#--Edit User

#--Edit Car

#--Edit Payment

#--Check transaction history (user)

#--Check entry exit (user)

#--Car enters
    #--Check if reg exists
    SELECT account_id FROM cars WHERE registration = "161LH122345";
    #--If it exists, add entry to car_entry table
    INSERT INTO car_entry(account_id, registration, image, datetime) VALUES (1007, "161LH12345", "2021-11-23,png", CURRENT_TIME)

    #--If barcode scanned
    SELECT account_id FROM users WHERE college_id = "d00321654"

    INSERT INTO car_entry(account_id, registration, datetime) VALUES (1007, "161LH12345", CURRENT_TIME)

    #--If ticket taken, print a ticket with barcode representing entry time. Ticket can be paid at a machine before leaving

#--Car Exits (Student id)

#--Car Exits (Ticket)

#--Car Exits  (Reg)

#--Delete Account