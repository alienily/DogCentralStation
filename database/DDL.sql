CREATE TABLE Customers (
    customerId int NOT NULL AUTO_INCREMENT,
    customerFirst varchar(145) NOT NULL,
    customerLast varchar(145) NOT NULL,
    joinDate date NOT NULL,
    email varchar(145),
    PRIMARY KEY (customerId)
);

CREATE TABLE Dogs (
    dogId int NOT NULL AUTO_INCREMENT,
    dogName varchar(145) NOT NULL,
    customerId int NOT NULL,
    size varchar(10) NOT NULL,
    useCaution int DEFAULT 0,
    dogNote varchar(145),
    PRIMARY KEY (dogId),
    CONSTRAINT fk_Dog_Owner FOREIGN KEY (customerId) REFERENCES Customers(customerId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Items (
    itemId int NOT NULL AUTO_INCREMENT,
    itemName varchar(145) NOT NULL,
    category varchar(145) NOT NULL,
    price decimal(4,2) NOT NULL,
    description varchar(145) NOT NULL,
    quantity int NOT NULL,
    PRIMARY KEY (itemId)
);

CREATE TABLE Employees(
    employeeId int NOT NULL AUTO_INCREMENT,
    employeeFirst varchar(145) NOT NULL,
    employeeLast varchar(145) NOT NULL,
    position varchar(45) NOT NULL,
    PRIMARY KEY (employeeId)
);

CREATE TABLE Appointments (
    appointmentId int NOT NULL AUTO_INCREMENT,
    appointmentDate datetime NOT NULL,
    employeeId int NOT NULL,
    dogId int NOT NULL,
    customerID int NOT NULL,
    treatment varchar(145) NOT NULL,
    PRIMARY KEY (appointmentId),
    CONSTRAINT fk_Customer_Appts FOREIGN KEY (customerId) REFERENCES Customers(customerId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Employee_Appts FOREIGN KEY (employeeId) REFERENCES Employees(employeeId) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_Dog_Appointments FOREIGN KEY (dogId) REFERENCES Dogs(dogId) ON DELETE RESTRICT 
);

CREATE TABLE Purchases (
    purchaseId int NOT NULL AUTO_INCREMENT,
    customerId int NOT NULL,
    employeeId int NOT NULL,
    appointmentId int,
    purchaseDate datetime NOT NULL,
    purchaseTotal decimal(4,2) NOT NULL,
    PRIMARY KEY (purchaseId),
    CONSTRAINT fk_Purchase_Customer FOREIGN KEY (customerId) REFERENCES Customers(customerId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Purchase_Employee FOREIGN KEY (employeeId) REFERENCES Employees(employeeId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Purchase_Appointment FOREIGN KEY (appointmentId) REFERENCES Appointments(appointmentId) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE PurchasesItemized (
    itemizedId int NOT NULL AUTO_INCREMENT,
    purchaseId int NOT NULL,
    itemId int NULL,
    itemQuantity int NULL,
    PRIMARY KEY (itemizedId),
    CONSTRAINT fk_Item_Has_Purchases FOREIGN KEY (purchaseId) REFERENCES Purchases(purchaseId) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_Purchase_Has_Items FOREIGN KEY (itemId) REFERENCES Items(itemId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Employees_has_Appointments (
   employeeId INT NOT NULL,
   appointmentId INT NOT NULL,
   PRIMARY KEY (employeeId, appointmentId),
   CONSTRAINT fk_Appointment_Has_Employees FOREIGN KEY (employeeId) REFERENCES  Employees(employeeId) ON DELETE CASCADE ON UPDATE CASCADE,
   CONSTRAINT fk_Employee_Has_Appointments FOREIGN KEY (appointmentId) REFERENCES Appointments(appointmentId) ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO Customers (customerFirst, customerLast, joinDate, email)
VALUES ('Lily', 'Zhou', '2020-06-22', 'lilyzhou@gmail.com' ),
('Mark', 'Hager', '2020-08-04', 'markhager@gmail.com'),
('Tiffany', 'Blue', '2021-02-21', 'tiffanyb1998@gmail.com'),
('Dwight', 'Schrute', '2021-02-24', 'bearsbeets@gmail.com'), 
('Parker', 'Lee', '2021-04-18', 'shinebright23@gmail.com');

INSERT INTO Dogs (dogName, customerId, size, useCaution, dogNote)
VALUES ('Clee', 1 , 'small', 0, NULL),
('Charlie', 2 , 'medium', 0, NULL),
('Porsche', 3, 'small', 1, "Be careful trimming around the face"),
('Paco', 4, 'small', 0, "Very nervous but has no teeth"), 
('Zuko', 5, 'large', 1, 'Needs 2 employees to wash');

INSERT INTO Items (itemName, category, price, description, quantity)
VALUES ('Sparkle Chews','Dental', 5.99 , 'Dog dental chew - pack of 2', 200),
('Gobbley Gibs for Small Dogs', 'Food', 20.99 , 'Turkey Chicken Kibble for small dogs', 96),
('Fowl Play Large Sized Squeak Toy', 'Toy', 16.99, 'Large sized goose', 23),
('Micro Pig for Micro Pups!', 'Toy', 9.99, 'Mini stuffed pig', 30);

INSERT INTO Employees (employeeFirst, employeeLast, position)
VALUES ('Alex', 'Kim', 'Manager'),
('Lexi', 'Wood' , 'Sales Associate'),
('Taylor', 'Grey', 'Sales Associate'),
('Oliver', 'Lee', 'Groomer'),
('Phoebe', 'Sanders', 'Groomer');


INSERT INTO Appointments (appointmentDate, employeeId, dogId, customerId, treatment)
VALUES ('2022-07-10 10:30:00', 2, 1, 1, 'Wash'),
('2022-07-10 11:30:00', 2, 2, 2, 'Wash'),
('2022-07-10 23:00:00', 3, 3, 3, 'Cut + Wash');


INSERT INTO Purchases (customerId, employeeId, appointmentId, purchaseDate, purchaseTotal)
VALUES (1, 2, NULL,'2022-02-10 10:34:09', 55.95),
(2, 2, NULL, '2022-03-04 13:30:02', 41.98),
(3, 3, NULL, '2022-07-11 12:22:05', 5.99),
(1, 2, 1, '2022-07-10 10:30:00', 59.99);


INSERT INTO PurchasesItemized (purchaseId, itemId, itemQuantity)
VALUES (1, 1, 3),
(1, 2, 1),
(1, 3, 1),
(2, 2, 2),
(3, 1, 1),
(4, NULL, NULL);

INSERT INTO Employees_has_Appointments (employeeId, appointmentId)
VALUES (2, 1), 
(2, 2), 
(3, 3)
