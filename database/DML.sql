-- CS 340 Intro to Databases
-- Project Step 3 Draft: DML
-- Kraken Coders
-- Members: Mark Hager, Lily Zhou

-- -----------------------------------------------------
-- 'Customers' Data Manipulation Queries
-- -----------------------------------------------------
-- get all customers's data to populate a dropdown for associating with a Customer
SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC

-- get all employee's data to populate a dropdown for associating with a Employee
SELECT employeeId FROM Employees ORDER BY employeeId ASC

-- get all item's data to populate a dropdown for associating with a Item
SELECT itemId, itemName FROM Items ORDER BY itemId ASC

-- get all purchases's data to populate a dropdown for associating with a Purchase
SELECT purchaseId FROM Purchases ORDER BY purchaseId ASC

-- get all dogs's data to populate a dropdown for associating with a Dog
SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC

-- get all appointment's data to populate a dropdown for associating with a Appointment
SELECT appointmentId FROM Appointments ORDER BY appointmentId ASC

-- Create
-- Add a new customer
INSERT INTO Customers (customerFirst, customerLast, joinDate, email)
VALUES (:customerFirstInput,
:customerLastInput,
:joinDateInput,
:emailInput)

-- READ
-- Get all customer information from the Customers table
SELECT * FROM Customers

-- UPDATE
-- Update a customer's information
-- 1. Get User
SELECT customerId, customerFirst, customerLast, joinDate, email FROM Customers
WHERE customerId = :customerId_selected_from_edit   -- User clicks on the edit button for the particular User's row

-- 2. Update User
UPDATE Customers
SET customerFirst = :customerFirstInput,
customerLast = :customerLastInput,
joinDate = :joinDateInput,
email = :emailInput
WHERE customerId = :customerId_selected_from_edit

--DELETE
-- Delete a customer's information
DELETE FROM Customers WHERE customerId = '%s'

-- -----------------------------------------------------
-- 'Dogs' Data Manipulation Queries
-- -----------------------------------------------------

-- Create
-- Add a new dog
INSERT INTO Dogs (dogName, customerId, size, useCaution, dogNote)
VALUES (:dogNameInput,
:customerId_from_dropdown_input)
:sizeInput,
:useCautionInput,
:dogNoteInput)

-- Read
-- Get all Dog Information from the Dogs table
SELECT * FROM Dogs

-- Update
-- Update Dogs information from the Dogs table
UPDATE Dogs
SET dogName = :dogNameInput,
customerId = :customerId_from_dropdown_input,
size = :sizeInput,
useCaution = :useCautionInput
dogNote = :dogNoteInput
WHERE dogId = :dogId_selected_from_edit

-- Delete
-- Delete Dog Information from the Dogs table

DELETE FROM Dogs WHERE dogId = '%s'

-- -----------------------------------------------------
-- 'Items' Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- Add a new Item

INSERT INTO Items (itemName, category, price, description, quantity)
VALUES (:itemNameInput,
:categoryInput,
:priceInput,
:descriptionInput,
quantityInput)

-- READ
-- Get all Item Information from the Items Table
SELECT * FROM Items

-- -----------------------------------------------------
-- 'Purchases' Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- Add a new Purchase

INSERT INTO Purchases (customerId, employeeId, appointmentId, purchaseDate, purchaseTotal)
VALUES (:customerId_from_dropdown_input,
:employeeId_from_dropdown_input,
:appointmentId_from_dropdown_input,
:purchaeDateInput,
:purchaseTotalInput)

-- READ
-- Get all Purchases Information from the Purchases Table
SELECT * FROM Purchases

-- -----------------------------------------------------
-- 'PurchasesItemized' Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- Add a new PurchasesItemized

INSERT INTO PurchasesItemized (purchaseId, itemId, itemQuantity)
VALUES (:purchaseId_from_dropdown_input,
:itemId_from_dropdown_input,
:itemQuantityInput)

-- READ
-- Get all PurchasesItemized Information from the PurchaesItemized Table
SELECT * FROM PurchasesItemized


-- -----------------------------------------------------
-- 'Employees' Data Manipulation Queries
-- -----------------------------------------------------
-- CREATE
-- Add a new Employee
INSERT INTO Employees (employeeFirst, employeeLast, position)
VALUES (:employeeFirstInput,
:employeeLastInput,
:position)


-- READ
-- Get all Employees information from the Employees Table
SELECT * FROM Employees

-- UPDATE
UPDATE Employees SET Employees.employeeFirst = %s, Employees.employeeLast = %s, Employees.position= %s  WHERE Employees.employeeId = %s

-- DELETE
DELETE FROM Employees WHERE employeeId = '%s'

-- -----------------------------------------------------
-- 'Appointments' Data Manipulation Queries
-- -----------------------------------------------------

-- CREATE
-- Add a new Appointment
INSERT INTO Appointments (appointmentDate, employeeId, dogId, dogName, customerId, treatment)
VALUES (:appointmentDateInput,
employeeId_from_dropdown_input,
:dogId_from_dropdown_input,
:dogName_from_dropdown_input,
:customerId_from_dropdown_input,
:treatment)

-- READ
-- Get all Appointment information from the Appointments Table

SELECT * FROM Appointments



-- Get employee name associated with appointment times
SELECT Employees.employeeId, Employees.employeeFirst, Appointments.appointmentId, Appointments.appointmentDate FROM Appointments
INNER JOIN Employees ON Appointments.employeeId = Employees.employeeId;

-- Get purchases connected to customers
SELECT Customers.customerFirst, Customers.customerId, Purchases.purchaseTotal, Purchases.purchaseDate FROM Customers
INNER JOIN Purchases ON Customers.customerId = Purchases.customerId;

-- Get CustomerId, Customer Name along with purchases and items in purchase
SELECT Customers.customerId, Customers.customerFirst, PurchasesItemized.itemQuantity, Items.itemName, Purchases.purchaseId, Purchases.purchaseTotal FROM Purchases
INNER JOIN Customers ON Purchases.customerId = Customers.customerId
INNER JOIN PurchasesItemized ON PurchasesItemized.purchaseId = Purchases.purchaseId
INNER JOIN Items ON PurchasesItemized.itemId = Items.itemId;

-- Get AppointmentId, employeeId, employeeFirst, appointmentDate, customerId, dogId, dogName, treatment, useCaution, dogNote
SELECT Appointments.appointmentId, Employees.employeeId, Employees.employeeFirst, Appointments.appointmentDate, Customers.customerId, Dogs.dogId, Dogs.dogName, Appointments.treatment, Dogs.useCaution, Dogs.dogNote FROM Appointments \
        INNER JOIN Customers ON Appointments.customerId = Customers.customerId\
        INNER JOIN Employees ON Appointments.employeeId = Employees.employeeId \
        INNER JOIN Dogs ON Appointments.dogId = Dogs.dogId\
        ORDER BY appointmentId ASC
-- -----------------------------------------------------
-- M:M Data Manipulation Queries
-- -----------------------------------------------------

UPDATE Appointments SET appointmentDate = :appointmentDateInput, dogId = :dogId_from_dropdown_Input, customerId = :customerId_from_dropdown_Input, treatment = :treatmentInput
WHERE appointmentId = :appointmentId_from_the_update_form

--UPDATE intersection table between Appointments and Employees
UPDATE Employees_has_Appointments SET Employees_has_Appointments.employeeId = %s WHERE Employees_has_Appointments.appointmentId = %s

--INSERT intertesction table between Appointments and Employees
INSERT INTO Employees_has_Appointments (appointmentId, employeeId)\
VALUES ((SELECT Appointments.appointmentId FROM Appointments WHERE appointmentDate =%s AND dogId = %s), %s)

-- -----------------------------------------------------
-- Delete Data Manipulation Queries
-- -----------------------------------------------------

-- dis-associate a appointment from a employee (M-to-M relationship deletion)
DELETE FROM Employees_has_Appointments where employeeId = :employeeId_selected_from_employee_and_appointment_list AND
appointmentId_selected_from_employee_and_appointment_list

DELETE FROM Customers WHERE customerId = :customerId_selected_from_browse_customer_page

