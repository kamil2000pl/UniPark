#--Test Queries

#--User Registration
#--When a user registers they enter full name, email and password
    #--check email has not already been used for an account
    SELECT COUNT(email_address) FROM accounts WHERE email_address = "d00321654@student.dkit.ie";
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
    #--Make sure that no more that 3 cars per account
    SELECT COUNT(registration) FROM cars WHERE account_id = 1;
    #--Make sure car is not already in db
    SELECT COUNT(registration) FROM cars WHERE registration = "161LH12345";
    #--Insert query
    INSERT INTO cars VALUES "212D111", 1005,
    "Could Not Add Record");

#--Add User

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