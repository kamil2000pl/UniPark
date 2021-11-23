#--Test Queries

#--User Registration
#--When a user registers they enter full name, email and password
    #--check email has not already been used for an account
    SELECT COUNT(email_address) FROM accounts WHERE email_address = "d00321654@student.dkit.ie";

    INSERT INTO #table1 (Id, guidd, TimeAdded, ExtraData)
    SELECT Id, guidd, TimeAdded, ExtraData
    FROM #table2
    WHERE NOT EXISTS (Select Id, guidd From #table1 WHERE #table1.id = #table2.id)

#--User Login
SELECT *
FROM users JOIN accounts USING (account_id)
WHERE users(email_address)

#--Add car
    #--Make sure that no more that 3 cars per account
    SELECT COUNT(registration) FROM cars WHERE account_id = 1;
    #--Make sure car is not already in db
    SELECT COUNT(registration) FROM cars WHERE registration = "161LH12345";

    #--Full combined query
    SELECT IF(COUNT(registration) FROM cars WHERE account_id = 1 < 3
    AND COUNT(registration) FROM cars WHERE registration = "161LH12345" = 0,
    INSERT INTO cars VALUES "212D111", 1005,
    "Could Not Add Record");

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