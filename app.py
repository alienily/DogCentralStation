"""
 Code credit goes to OSU and the authors of CS340 starter BSG code as well as the Flask template instructions
 https://github.com/osu-cs340-ecampus/flask-starter-app
"""
from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os
import database.db_connector as db


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_zhoulil'
app.config['MYSQL_PASSWORD'] = '8410'
app.config['MYSQL_DB'] = 'cs340_zhoulil'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# ---------------------------------------------------------------------------
# Index/Homepage Route
# ---------------------------------------------------------------------------
@app.route('/')
def root():
    return render_template("index.html")

# ---------------------------------------------------------------------------
# Customers Table Routes
# ---------------------------------------------------------------------------
@app.route('/customers.html', methods = ["POST", "GET"])
def customers():
    if request.method == "POST":
        # fire off if user presses the Add Customer button
        if request.form.get("addCustomer"):
            #grab user form inputs
            customerFirst = request.form["customerFirst"]
            customerLast = request.form["customerLast"]
            joinDate = request.form["joinDate"]
            email = request.form["email"]

            # account for null email
            if email == "":
                query = "INSERT INTO Customers (customerFirst, customerLast, joinDate) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (customerFirst, customerLast, joinDate))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Customers (customerFirst, customerLast, joinDate, email) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (customerFirst, customerLast, joinDate, email))
                mysql.connection.commit()

            # redirect back to customers page
            return redirect('/customers.html')


       # Search Customers
        elif request.form.get("searchCustomers"):
            nameSearch = request.form["customerName"]
            emailSearch = request.form["customerEmail"]
            if nameSearch != '' and emailSearch == '':
                query = f"SELECT * FROM `Customers` WHERE concat_ws(' ', customerFirst, customerLast) like '%{nameSearch}%';"
            elif emailSearch != '' and nameSearch == '':
                query = f"SELECT * FROM `Customers` WHERE email = '{emailSearch}';"
            else:
                query = f"SELECT * FROM `Customers` WHERE concat_ws(' ', customerFirst, customerLast) like '%{nameSearch}%' AND email = '{emailSearch}';"

            cur = mysql.connection.cursor()
            cur.execute(query)
            results = cur.fetchall()

            #mySQL query to grab id/name data for our Customers dropdown
            query2 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            customersInfo = cur.fetchall()

            return render_template("customers.html", Customers=results, customersInfo = customersInfo)

    if request.method == "GET":
        query = "SELECT * FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our Customers dropdown
        query2 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customersInfo = cur.fetchall()

        return render_template("customers.html", Customers=results, customersInfo = customersInfo)

# DELETE Customer
@app.route("/deleteCustomer/<int:customerId>")
def deleteCustomer(customerId):
    query = "DELETE FROM Customers WHERE customerId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customerId,))
    mysql.connection.commit()
    return redirect("/customers.html")


# route for edit functionality, updating the attributes of a customer in Customers
# similar to our delete route, we want to the pass the 'id' value of that customer on button click (see HTML) via the route
@app.route("/updateCustomer/<int:customerId>", methods=["POST", "GET"])
def updateCustomer(customerId):
    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Update Customer' button
        if request.form.get("updateCustomer"):
            # grab user form inputs
            customerId = request.form["customerId"]
            customerFirst = request.form["customerFirst"]
            customerLast = request.form["customerLast"]
            joinDate = request.form["joinDate"]
            email = request.form["email"]

            # if email is NULL
            if email == "":
                query = "UPDATE Customers SET Customers.customerFirst = %s, Customers.customerLast = %s, Customers.joinDate = %s, Customers.email = NULL WHERE Customers.customerId = %s "
                cur = mysql.connection.cursor()
                cur.execute(query, (customerFirst, customerLast, joinDate, customerId))
                mysql.connection.commit()

            else:
                query = "UPDATE Customers SET Customers.customerFirst = %s, Customers.customerLast = %s, Customers.joinDate = %s, Customers.email = %s WHERE Customers.customerId = %s "
                cur = mysql.connection.cursor()
                cur.execute(query, (customerFirst, customerLast, joinDate, email, customerId))
                mysql.connection.commit()

        return redirect("/customers.html")

    if request.method == "GET":
        # mySQL query to grab the info of the customer with our passed id
        query = "SELECT * FROM Customers WHERE customerId = %s" % (customerId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        # mySQL query to grab customer id/name data for our dropdown
        query2 = "SELECT customerId, customerFirst FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        customersInfo = cur.fetchall()

        # render updateCustomer page passing our query data)
        return render_template("updateCustomer.html", Customers=results, customersInfo=customersInfo)

# ---------------------------------------------------------------------------
# Dogs Table Routes
# ---------------------------------------------------------------------------
@app.route('/dogs.html', methods = ["POST", "GET"])
def dogs():
    if request.method == "POST":
        # fire off if user presses the Add Dog button
        if request.form.get("addDog"):
            #grab user form inputs
            dogName = request.form["dogName"]
            customerId = request.form["customerId"]
            size = request.form["size"]
            useCaution = request.form["useCaution"]
            dogNote = request.form["dogNote"]

            # if dogNote is NULL
            if dogNote == "":
                query = "INSERT INTO Dogs (dogName, customerId, size, useCaution) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (dogName, customerId, size, useCaution))
                mysql.connection.commit()

            else:
                query = "INSERT INTO Dogs (dogName, customerId, size, useCaution, dogNote) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (dogName, customerId, size, useCaution, dogNote))
                mysql.connection.commit()

            return redirect("/dogs.html")

        elif request.form.get("searchDogs"):
            nameSearch = request.form["dogName"]

            query = f"SELECT * FROM `Dogs` WHERE dogName like '%{nameSearch}%';"
            cur = mysql.connection.cursor()
            cur.execute(query)
            results = cur.fetchall()

            #mySQL query to grab id/name data for our Employees dropdown
            query2 = "SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC;"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            itemsInfo = cur.fetchall()

            return render_template("dogs.html", Dogs=results, DogsInfo = itemsInfo)


    if request.method == "GET":
        query = "SELECT dogId, dogName, Customers.customerId, Customers.customerFirst, size, if(useCaution, 'YES', 'No'), dogNote FROM Dogs INNER JOIN Customers ON Dogs.customerId = Customers.customerId;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our DOGS dropdown
        query2 = "SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        dogsInfo = cur.fetchall()

        #mySQL query to grab id/name data for our Customers dropdown
        query3 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        customersInfo = cur.fetchall()

        return render_template("dogs.html", Dogs=results, dogsInfo = dogsInfo, customersInfo = customersInfo)

@app.route("/updateDog/<int:dogId>", methods=["POST", "GET"])
def updateDog(dogId):
    # meat and potatoes of our update functionality

    if request.method == "POST":
        # fire off if user clicks the 'Update Dog' button
              # UPDATE Dog
        if request.form.get("updateDog"):
            dogId = request.form["dogId"]
            dogName = request.form["dogName"]
            customerId = request.form["customerId"]
            size = request.form["size"]
            useCaution = request.form["useCaution"]
            dogNote = request.form["dogNote"]

            # if dogNote is NULL
            if dogNote == "":
                query = "UPDATE Dogs SET Dogs.dogName = %s, Dogs.customerId = %s, Dogs.size = %s, Dogs.useCaution = %s, Dogs.dogNote = NULL WHERE Dogs.dogId = %s "
                cur = mysql.connection.cursor()
                cur.execute(query, (dogName, customerId, size, useCaution, dogId))
                mysql.connection.commit()

            else:
                query = "UPDATE Dogs SET Dogs.dogName = %s, Dogs.customerId = %s, Dogs.size = %s, Dogs.useCaution = %s, Dogs.dogNote = %s WHERE Dogs.dogId = %s "
                cur = mysql.connection.cursor()
                cur.execute(query, (dogName, customerId, size, useCaution, dogNote, dogId))
                mysql.connection.commit()

            return redirect("/dogs.html")

    if request.method == "GET":
        query = "SELECT dogId, dogName, Customers.customerId, Customers.customerFirst, size, if(useCaution, 'YES', 'No'), dogNote FROM Dogs INNER JOIN Customers ON Dogs.customerId = Customers.customerId \
        WHERE dogId = %s" % (dogId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our DOGS dropdown
        query2 = "SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        dogsInfo = cur.fetchall()

        #mySQL query to grab id/name data for our Customers dropdown
        query3 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        customersInfo = cur.fetchall()

        return render_template("updateDog.html", Dogs=results, dogsInfo = dogsInfo, customersInfo = customersInfo)

@app.route("/deleteDog/<int:dogId>")
def deleteDog(dogId):
    query = "DELETE FROM Dogs WHERE dogId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (dogId,))
    mysql.connection.commit()
    return redirect("/dogs.html")

# ---------------------------------------------------------------------------
# Items Table Routes
# ---------------------------------------------------------------------------
@app.route('/items.html', methods = ["POST", "GET"])
def items():
    if request.method == "POST":
        # fire off if user presses the Add Item button
        if request.form.get("addItem"):
            #grab user form inputs
            itemName = request.form["itemName"]
            category = request.form["category"]
            price = request.form["price"]
            description = request.form["description"]
            quantity = request.form["quantity"]

            query = "INSERT INTO Items (itemName, category, price, description, quantity) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (itemName, category, price, description, quantity))
            mysql.connection.commit()

            return redirect("/items.html")

        elif request.form.get("searchItems"):
            nameSearch = request.form["itemName"]

            query = f"SELECT * FROM `Items` WHERE itemName like '%{nameSearch}%';"
            cur = mysql.connection.cursor()
            cur.execute(query)
            results = cur.fetchall()

            #mySQL query to grab id/name data for our Employees dropdown
            query2 = "SELECT itemId, itemName FROM Items ORDER BY itemId ASC;"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            itemsInfo = cur.fetchall()

            return render_template("items.html", Items=results, ItemsInfo = itemsInfo)

    if request.method == "GET":
        query = "SELECT itemId, itemName, category, price, description, quantity FROM Items ;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our Items dropdown
        query2 = "SELECT itemId, itemName FROM Items ORDER BY itemId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        itemsInfo = cur.fetchall()

        return render_template("items.html", Items=results, itemsInfo = itemsInfo)


@app.route("/updateItem/<int:itemId>", methods=["POST", "GET"])
def updateItem(itemId):
    if request.method == "POST":
        if request.form.get("updateItem"):
            itemId = request.form["itemId"]
            itemName = request.form["itemName"]
            category = request.form["category"]
            price = request.form["price"]
            description = request.form["description"]
            quantity = request.form["quantity"]

            query = "UPDATE Items SET Items.itemName = %s, Items.category = %s, Items.price = %s, Items.description = %s, Items.quantity = %s WHERE Items.itemId = %s "
            cur = mysql.connection.cursor()
            cur.execute(query, (itemName, category, price, description, quantity, itemId))
            mysql.connection.commit()

        return redirect("/items.html")

    if request.method == "GET":
        query = "SELECT itemId, itemName, category, price, description, quantity FROM Items WHERE itemId = %s" % (itemId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our Items dropdown
        query2 = "SELECT itemId, itemName FROM Items ORDER BY itemId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        itemsInfo = cur.fetchall()

        return render_template("updateItem.html", Items=results, itemsInfo = itemsInfo)

@app.route("/deleteItem/<int:itemId>")
def deleteItem(itemId):
    query = "DELETE FROM Items WHERE itemId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (itemId,))
    mysql.connection.commit()
    return redirect("/items.html")

# ---------------------------------------------------------------------------
# Purchases Table Routes
# ---------------------------------------------------------------------------
@app.route('/purchases.html', methods = ["POST", "GET"])
def purchases():
    if request.method == "POST":
        if request.form.get("addPurchase"):
           #grab user form inputs
           #grab user form inputs
            purchaseId = request.form["purchaseId"]
            itemId = request.form["itemId"]
            itemQuantity = request.form["itemizedQuantity"]


            # INSERT INTO intersection table PurchasesItemized M:M
            query2 = "INSERT INTO PurchasesItemized (purchaseId, itemId, itemQuantity) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query2, (purchaseId, itemId, itemQuantity))
            mysql.connection.commit()
            # redirect back to purchases page
            return redirect('/purchases.html')


    if request.method == "GET":
        query = "SELECT Purchases.purchaseId, PurchasesItemized.itemizedId, Items.itemId, Appointments.appointmentId, Customers.customerId, Items.itemName, PurchasesItemized.itemQuantity, Purchases.purchaseDate, Purchases.purchaseTotal FROM Purchases \
        INNER JOIN Customers ON Purchases.customerId = Customers.customerId \
        INNER JOIN Appointments ON Appointments.customerId = Customers.customerId \
        INNER JOIN PurchasesItemized ON PurchasesItemized.purchaseId = Purchases.purchaseId \
        INNER JOIN Items ON PurchasesItemized.itemId = Items.itemId ;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id data for our employeeId dropdown
        query1 = "SELECT employeeId, employeeFirst, employeeLast FROM Employees ORDER BY employeeId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        employeesInfo = cur.fetchall()

        # mySQL query to grab id data for our purchaseId dropdown
        query2 = "SELECT purchaseId FROM Purchases ORDER BY purchaseId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        purchasesInfo = cur.fetchall()

        # mySQL query to grab id/name data for our purchasesItemized dropdown
        query3 = "SELECT itemizedId FROM PurchasesItemized ORDER BY itemizedId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        itemizedInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Items dropdown
        query4 = "SELECT itemId, itemName FROM Items ORDER BY itemId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        itemsInfo = cur.fetchall()

        # mySQL query to grab id data for our Appointments dropdown
        query5 = "SELECT appointmentId, treatment FROM Appointments ORDER BY appointmentId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        appointmentsInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Customer dropdown
        query6 = "SELECT customerId, customerFirst, customerLast FROM Customers ORDER BY customerId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query6)
        customersInfo = cur.fetchall()

        return render_template("purchases.html", Purchases=results, purchasesInfo = purchasesInfo, itemizedInfo = itemizedInfo, \
        itemsInfo = itemsInfo, appointmentsInfo = appointmentsInfo, customersInfo = customersInfo, employeesInfo = employeesInfo)


@app.route("/deletePurchase/<int:purchaseId>")
def deletePurchase(purchaseId):
    query = "DELETE FROM Purchases WHERE purchaseId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (purchaseId,))
    mysql.connection.commit()
    return redirect("/purchases.html")


# WORK IN PROGRESS
@app.route("/updatePurchase/<int:purchaseId>", methods=["POST", "GET"])
def updatePurchase(purchaseId):
    if request.method == "POST":
        if request.form.get("updatePurchase"):
            #grab user form inputs
            purchaseId = request.form["purchaseId"]
            itemizedId = request.form["itemizedId"]
            itemId = request.form["itemId"]
            appointmentId = request.form["appointmentId"]
            customerId = request.form["customerId"]
            itemQuantity = request.form["itemizedQuantity"]
            itemName = request.form["itemName"]
            itemQuantity = request.form["itemQuantity"]
            purchaseDate = request.form["purchaseDate"]
            purchaseTotal = request.form["purchaseTotal"]

            query = "UPDATE Purchases SET Purchases.purchaseId = %s, Items.itemId = %s, Items.itemQuantity = %s WHERE PurchasesIte.appointmentId = %s "
            cur = mysql.connection.cursor()
            cur.execute(query, (purchaseId, itemId, itemQuantity))
            mysql.connection.commit()

            # UPDATE M:M Relationship, by updating Intersection table
            query2 = "UPDATE PurchasesItemized SET Employees_has_Appointments.employeeId = %s WHERE Employees_has_Appointments.appointmentId = %s"
            cur = mysql.connection.cursor()
            cur.execute(query2, (employeeId, appointmentId))
            mysql.connection.commit()

            return redirect("/purchases.html")

    if request.method == "GET":
        query = "SELECT Purchases.purchaseId, PurchasesItemized.itemizedId, Items.itemId, Appointments.appointmentId, Employees.employeeId, Customers.customerId, Items.itemName, PurchasesItemized.itemQuantity, Purchases.purchaseDate, Purchases.purchaseTotal FROM Purchases \
        INNER JOIN Employees ON Purchases.employeeId = Employees.employeeId \
        INNER JOIN Customers ON Purchases.customerId = Customers.customerId \
        INNER JOIN Appointments ON Appointments.customerId = Customers.customerId \
        INNER JOIN PurchasesItemized ON PurchasesItemized.purchaseId = Purchases.purchaseId \
        INNER JOIN Items ON PurchasesItemized.itemId = Items.itemId \
        WHERE Purchases.purchaseId = %s" % (purchaseId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id data for our employeeId dropdown
        query1 = "SELECT employeeId, employeeFirst, employeeLast FROM Employees ORDER BY employeeId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        employeesInfo = cur.fetchall()

        # mySQL query to grab id data for our purchaseId dropdown
        query2 = "SELECT purchaseId FROM Purchases ORDER BY purchaseId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        purchasesInfo = cur.fetchall()

        # mySQL query to grab id/name data for our purchasesItemized dropdown
        query3 = "SELECT itemizedId FROM PurchasesItemized ORDER BY itemizedId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        itemizedInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Items dropdown
        query4 = "SELECT itemId, itemName FROM Items ORDER BY itemId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        itemsInfo = cur.fetchall()

        # mySQL query to grab id data for our Appointments dropdown
        query5 = "SELECT appointmentId, treatment FROM Appointments ORDER BY appointmentId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        appointmentsInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Customer dropdown
        query6 = "SELECT customerId, customerFirst, customerLast FROM Customers ORDER BY customerId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query6)
        customersInfo = cur.fetchall()

        return render_template("updatePurchase.html", Purchases=results, purchasesInfo = purchasesInfo, itemizedInfo = itemizedInfo, \
        itemsInfo = itemsInfo, appointmentsInfo = appointmentsInfo, customersInfo = customersInfo, employeesInfo = employeesInfo)

# ---------------------------------------------------------------------------
# Employees Table Routes
# ---------------------------------------------------------------------------
@app.route('/employees.html', methods = ["POST", "GET"])
def employees():
    if request.method == "POST":
        # fire off if user presses the Add Employee button
        if request.form.get("addEmployee"):
            #grab user form inputs
            employeeFirst = request.form["employeeFirst"]
            employeeLast = request.form["employeeLast"]
            position = request.form["position"]

            query = "INSERT INTO Employees (employeeFirst, employeeLast, position) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (employeeFirst, employeeLast, position))
            mysql.connection.commit()

            return redirect("/employees.html")

        elif request.form.get("searchEmployees"):
            nameSearch = request.form["employeeName"]

            query = f"SELECT * FROM `Employees` WHERE concat_ws(' ', employeeFirst, employeeLast) like '%{nameSearch}%';"
            cur = mysql.connection.cursor()
            cur.execute(query)
            results = cur.fetchall()

            #mySQL query to grab id/name data for our Employees dropdown
            query2 = "SELECT employeeId, employeeFirst FROM Employees ORDER BY employeeId ASC;"
            cur = mysql.connection.cursor()
            cur.execute(query2)
            employeesInfo = cur.fetchall()

            return render_template("employees.html", Employees=results, employeesInfo = employeesInfo)
    if request.method == "GET":
        query = "SELECT employeeId, employeeFirst, employeeLast, position FROM Employees ;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our Items dropdown
        query2 = "SELECT employeeId, employeeFirst FROM Employees ORDER BY employeeId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        employeesInfo = cur.fetchall()

        return render_template("employees.html", Employees=results, employeesInfo = employeesInfo)

@app.route("/deleteEmployee/<int:employeeId>")
def deleteEmployee(employeeId):
    query = "DELETE FROM Employees WHERE employeeId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (employeeId,))
    mysql.connection.commit()
    return redirect("/employees.html")


@app.route("/updateEmployee/<int:employeeId>", methods=["POST", "GET"])
def updateEmployee(employeeId):
    if request.method == "POST":
        if request.form.get("updateEmployee"):
            itemId = request.form["employeeId"]
            employeeFirst = request.form["employeeFirst"]
            employeeLast = request.form["employeeLast"]
            position = request.form["position"]

            query = "UPDATE Employees SET Employees.employeeFirst = %s, Employees.employeeLast = %s, Employees.position= %s  WHERE Employees.employeeId = %s "
            cur = mysql.connection.cursor()
            cur.execute(query, (employeeFirst, employeeLast, position, employeeId))
            mysql.connection.commit()


        return redirect("/employees.html")

    if request.method == "GET":
        query = "SELECT employeeId, employeeFirst, employeeLast, position FROM Employees WHERE employeeId = %s" % (employeeId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        #mySQL query to grab id/name data for our Items dropdown
        query2 = "SELECT employeeId, employeeFirst FROM Employees ORDER BY employeeId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        employeesInfo = cur.fetchall()

        return render_template("updateEmployee.html", Employees=results, employeesInfo = employeesInfo)

# ---------------------------------------------------------------------------
# Appointments Table Routes
# ---------------------------------------------------------------------------
@app.route('/appointments.html', methods = ["POST", "GET"])
def appointments():
    if request.method == "POST":
        if request.form.get("addAppointment"):
            #grab user form inputs
            appointmentDate = request.form["appointmentDate"]
            dogId = request.form["dogId"]
            customerId = request.form["customerId"]
            employeeId = request.form["employeeId"]
            treatment = request.form["treatment"]

            query = "INSERT INTO Appointments (appointmentDate, employeeId, customerId, dogId, treatment) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (appointmentDate, employeeId, customerId, dogId, treatment))
            mysql.connection.commit()

            # INSERT INTO intersection table Employees_has_Appointments M:M
            query2 = "INSERT INTO Employees_has_Appointments (appointmentId, employeeId)\
             VALUES ((SELECT Appointments.appointmentId FROM Appointments WHERE appointmentDate =%s AND dogId = %s), %s);"
            cur = mysql.connection.cursor()
            cur.execute(query2, (appointmentDate, dogId, employeeId))
            mysql.connection.commit()

            # redirect back to appointments page
            return redirect('/appointments.html')

    if request.method == "GET":
        query = "SELECT Appointments.appointmentId, Employees.employeeId, Employees.employeeFirst, Appointments.appointmentDate, Customers.customerId, Dogs.dogId, Dogs.dogName, Appointments.treatment, Dogs.useCaution, Dogs.dogNote FROM Appointments \
        INNER JOIN Customers ON Appointments.customerId = Customers.customerId\
        INNER JOIN Employees ON Appointments.employeeId = Employees.employeeId \
        INNER JOIN Dogs ON Appointments.dogId = Dogs.dogId\
        ORDER BY appointmentId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        # mySQL query to grab id/name data for our Employees dropdown
        query2 = "SELECT employeeId, employeeFirst FROM Employees ORDER BY employeeId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        employeesInfo = cur.fetchall()

        # mySQL query to grab dog id/name data for our Dogs dropdown
        query3 = "SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        dogsInfo = cur.fetchall()

        # mySQL query to grab id data for our Appointments dropdown
        query4 = "SELECT appointmentId FROM Appointments ORDER BY appointmentId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        appointmentsInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Customers dropdown
        query5 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        customersInfo = cur.fetchall()

        return render_template("appointments.html", Appointments=results, appointmentsInfo = appointmentsInfo, dogsInfo = dogsInfo, \
        employeesInfo = employeesInfo, customersInfo = customersInfo)

@app.route("/deleteAppointment/<int:appointmentId>")
def deleteAppointment(appointmentId):
    query = "DELETE FROM Appointments WHERE appointmentId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (appointmentId,))
    mysql.connection.commit()

    # DELETE M:M from intersection table
    query2 = "DELETE FROM Employees_has_Appointments WHERE appointmentId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query2, (appointmentId,))
    mysql.connection.commit()

    return redirect("/appointments.html")

@app.route("/updateAppointment/<int:appointmentId>", methods=["POST", "GET"])
def updateAppointment(appointmentId):
    if request.method == "POST":
        if request.form.get("updateAppointment"):
            #grab user form inputs
            appointmentDate = request.form["appointmentDate"]
            dogId = request.form["dogId"]
            customerId = request.form["customerId"]
            employeeId = request.form["employeeId"]
            treatment = request.form["treatment"]

        query = "UPDATE Appointments SET Appointments.appointmentDate = %s, Appointments.customerId = %s, Appointments.employeeId = %s, Appointments.dogId = %s, Appointments.treatment = %s WHERE Appointments.appointmentId = %s "
        cur = mysql.connection.cursor()
        cur.execute(query, (appointmentDate, customerId, dogId, employeeId, treatment, appointmentId))
        mysql.connection.commit()

        # UPDATE M:M Relationship, by updating Intersection table
        query2 = "UPDATE Employees_has_Appointments SET Employees_has_Appointments.employeeId = %s WHERE Employees_has_Appointments.appointmentId = %s"
        cur = mysql.connection.cursor()
        cur.execute(query2, (employeeId, appointmentId))
        mysql.connection.commit()

        return redirect("/appointments.html")

    if request.method == "GET":
        query = "SELECT Appointments.appointmentId, Employees.employeeId, Employees.employeeFirst, Appointments.appointmentDate, Customers.customerId, Dogs.dogId, Dogs.dogName, Appointments.treatment, Dogs.useCaution, Dogs.dogNote FROM Appointments \
        INNER JOIN Customers ON Appointments.customerId = Customers.customerId \
        INNER JOIN Employees ON Appointments.employeeId = Employees.employeeId \
        INNER JOIN Dogs ON Appointments.dogId = Dogs.dogId \
        WHERE appointmentId = %s" % (appointmentId)
        cur = mysql.connection.cursor()
        cur.execute(query)
        results = cur.fetchall()

        # mySQL query to grab id/name data for our Employees dropdown
        query2 = "SELECT employeeId, employeeFirst FROM Employees ORDER BY employeeId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        employeesInfo = cur.fetchall()

        # mySQL query to grab dog id/name data for our Dogs dropdown
        query3 = "SELECT dogId, dogName FROM Dogs ORDER BY dogId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        dogsInfo = cur.fetchall()

        # mySQL query to grab id data for our Appointments dropdown
        query4 = "SELECT appointmentId FROM Appointments ORDER BY appointmentId ASC"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        appointmentsInfo = cur.fetchall()

        # mySQL query to grab id/name data for our Customers dropdown
        query5 = "SELECT customerId, customerFirst FROM Customers ORDER BY customerId ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        customersInfo = cur.fetchall()

        return render_template("updateAppointment.html", Appointments=results, appointmentsInfo = appointmentsInfo, dogsInfo = dogsInfo, \
        employeesInfo = employeesInfo, customersInfo = customersInfo)

# Listener
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 9112))
    #Start the app on port 3000, it will be different once hosted
    app.run(port=43000, debug=True)