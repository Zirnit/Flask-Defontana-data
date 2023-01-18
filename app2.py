import requests
from flask import Flask, request
import mysql.connector
import os
from dotenv import load_dotenv
from get_def_data import get_def_data, get_order_data

# Load environment variables from .env file
load_dotenv()

# HTTP headers to use when making API requests
dKey = os.getenv('dKey')

# MySQL connection details
mysql_host = os.getenv('MYSQL_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_db = os.getenv('MYSQL_DB')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Flask app!'

@app.route('/populate_orders')
def populate_orders():
    # Connect to MySQL database
    connection = mysql.connector.connect(host=mysql_host,
                                        user=mysql_user,
                                        password=mysql_password,
                                        database=mysql_db)

    response = get_def_data()
    # Iterate over the orders and insert them into the MySQL database
    for item in response['items']:
        order = get_order_data(item['number'])['orderData']
        print(order)
        cursor = connection.cursor()
        sql = '''INSERT INTO orders (document_type_id, number, client_file_id, client_legal_code,
                                     client_name, client_giro, client_address, client_country,
                                     client_city, client_region, client_district, client_email,
                                     client_phone, creation_date, shop_id, billing_coind_id,
                                     billing_rate, seller_id, expiration_date, comment,
                                     billing_comment, dispatch_comment, success, message,
                                     exception_message)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        values = (order['documentTypeID'], order['number'], order['clientFileId'], order['clientLegalCode'],
                  order['clientName'], order['clientGiro'], order['clientAddress'], order['clientCountry'],
                  order['clientCity'], order['clientRegion'], order['clientDistrict'], order['clientEmail'],
                  order['clientPhone'], order['creationDate'], order['shopID'], order['billingCoindID'],
                  order['billingRate'], order['sellerID'], order['expirationDate'], order['comment'],
                  order['billingComment'], order['dispatchComment'], response['success'], response['message'],
                  response['exceptionMessage'])
        cursor.execute(sql, values)
        connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return "Updated database"

if __name__ == '__main__':
    app.run()