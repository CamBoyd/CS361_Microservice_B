# Make necessary imports
import os
import flask_mysqldb
from flask import *
import flask
import csv
import datetime


# Initialize web app here so database can be intialized. Imported in app.py.
app = Flask(__name__)

# Continue with database initialization using secret username / password.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'CarbonCrash'
app.config['MYSQL_DB'] = 'invoicetracking'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.config['SECRET_KEY'] = 'secret!'
mysql = flask_mysqldb.MySQL(app)

# Routes

@app.route('/', methods=["POST"])
def home():
    data = request.json
    recordType = data.get("recordType")
    record = data.get("record")
    if recordType == "AR":
        ar_invoices_insert_query(record)
    if recordType == "AP":
        ap_invoices_insert_query(record)

    return "Microservice B"

def ar_invoices_insert_query(ARRecord):
    invoice = ARRecord[0]
    customerName = ARRecord[1]
    description = ARRecord[2]
    invoiceDate = datetime.datetime.strptime(ARRecord[3], "%m/%d/%Y")
    dueDate = datetime.datetime.strptime(ARRecord[4], "%m/%d/%Y")
    amount = ARRecord[5]
    query = """
        INSERT INTO ARInvoices
        (
            Invoice,
            CustomerName,
            Description,
            InvoiceDate,
            DueDate,
            Amount
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        """
    cursor = mysql.connection.cursor()
    cursor.execute(query, (invoice, customerName, description, invoiceDate, dueDate, amount))
    mysql.connection.commit()

def ap_invoices_insert_query(APRecord):
    invoice = APRecord[0]
    vendorName = APRecord[1]
    description = APRecord[2]
    invoiceDate = datetime.datetime.strptime(APRecord[3], "%m/%d/%Y")
    dueDate = datetime.datetime.strptime(APRecord[4], "%m/%d/%Y")
    amount = APRecord[5]
    query = """
        INSERT INTO APInvoices
        (
            Invoice,
            VendorName,
            Description,
            InvoiceDate,
            DueDate,
            Amount
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        );
        """
    cursor = mysql.connection.cursor()
    cursor.execute(query, (invoice, vendorName, description, invoiceDate, dueDate, amount))
    mysql.connection.commit()

# Listener

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 50001)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    #app.run(port=port)
    app.run(port=port, debug=True)