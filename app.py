import os
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import get_def_data as GD
import db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Connect to the MySQL database using the connection details from the .env file
cnx = mysql.connector.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'),
                              host=os.getenv('MYSQL_HOST'), database=os.getenv('MYSQL_DB'))
cursor = cnx.cursor()

# Function to update the database with data from the API
def update_database():
    # Actualiza artículos
    articulos = GD.obtener_articulos()
    for item in articulos:
        if item["code"]:
            db.cargar_articulos(item)
    categorias = GD.obtener_categorías()
    for item in categorias:
        if item["categoryID"]:
            db.cargar_categorias(item)
    stock_por_recibir = GD.obtener_stock_futuro()
    for item in stock_por_recibir:
        if item["productCode"]:
            db.cargar_stock_futuro(item)
    # ordenes_compra = GD.obtener_orden_compras()
    # for item in ordenes_compra:
    #     if item["number"]:
    #         db.cargar_orden_compra(item)

# Function to update the database with detailed data for a specific order
def update_order_data(order_number):
    # Fetch the detailed data for the order from the API
    order_data = GD.get_order_data(order_number)

    # Check if the order already exists in the database
    cursor.execute("SELECT * FROM detalle_pedido WHERE number = %s", (order_number,))
    result = cursor.fetchone()
    if result is None:
        # Insert the order into the database
        cursor.execute("INSERT INTO detalle_pedido (number, document_type_id, client_file_id, client_name, client_giro, client_address, client_country, client_city, client_region, client_district, client_email, client_phone, creation_date, shop_id, billing_coind_id, billing_rate, seller_id, expiration_date, coment, billing_comment, dispatch_comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (order_number, order_data["orderData"]["documentTypeID"], order_data["orderData"]["client"]["fileId"], order_data["orderData"]["client"]["name"], order_data["orderData"]["client"]["giro"], order_data["orderData"]["client"]["address"], order_data["orderData"]["client"]["country"], order_data["orderData"]["client"]["city"], order_data["orderData"]["client"]["region"], order_data["orderData"]["client"]["district"], order_data["orderData"]["client"]["email"], order_data["orderData"]["client"]["phone"], order_data["orderData"]["creationDate"], order_data["orderData"]["shopID"], order_data["orderData"]["billingCoindID"], order_data["orderData"]["billingRate"], order_data["orderData"]["sellerID"], order_data["orderData"]["expirationDate"], order_data["orderData"]["comment"], order_data["orderData"]["billingComment"], order_data["orderData"]["dispatchComment"]))
        cnx.commit()
    else:
        # Update the existing order in the database
        cursor.execute("UPDATE detalle_pedido SET document_type_id = %s, client_file_id = %s, client_name = %s, client_giro = %s, client_address = %s, client_country = %s, client_city = %s, client_region = %s, client_district = %s, client_email = %s, client_phone = %s, creation_date = %s, shop_id = %s, billing_coind_id = %s, billing_rate = %s, seller_id = %s, expiration_date = %s, coment = %s, billing_comment = %s, dispatch_comment = %s WHERE number = %s", (order_data["orderData"]["documentTypeID"], order_data["orderData"]["client"]["fileId"], order_data["orderData"]["client"]["name"], order_data["orderData"]["client"]["giro"], order_data["orderData"]["client"]["address"], order_data["orderData"]["client"]["country"], order_data["orderData"]["client"]["city"], order_data["orderData"]["client"]["region"], order_data["orderData"]["client"]["district"], order_data["orderData"]["client"]["email"], order_data["orderData"]["client"]["phone"], order_data["orderData"]["creationDate"], order_data["orderData"]["shopID"], order_data["orderData"]["billingCoindID"], order_data["orderData"]["billingRate"], order_data["orderData"]["sellerID"], order_data["orderData"]["expirationDate"], order_data["orderData"]["comment"], order_data["orderData"]["billingComment"], order_data["orderData"]["dispatchComment"], order_number))
        cnx.commit()

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Update the database with data from the API
        update_database()
    return render_template('index.html')
    

# Route for the detailed order page
@app.route('/detalle_pedido/<order_number>')
def detalle_pedido(order_number):
    update_order_data(order_number)
    # Query the database to get the detailed data for the specified order
    cursor.execute("SELECT * FROM detalle_pedido WHERE number = %s", (order_number,))
    result = cursor.fetchone()

    # Render the template with the detailed data
    print(result)
    # return render_template('detalle_pedido.html', data=result)

@app.route('/articulos', methods=["GET","POST"])
def articulos():
    if request.method == 'POST':
        # Update the database with data from the API
        update_database()
    # Execute the SELECT query
    valid_columns = {
    '0': 'id_articulo',
    '1': 'nombre',
    '2': 'unidad_venta',
    '3': 'nombre_categoria',
    '4': 'stock_actual',
    '5': 'stock_reservado',
    '6': 'stock_por_recibir',
    '7': 'stock_futuro'
    }

    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order')
    if sort_column and sort_column in valid_columns and sort_order in ('asc', 'desc'):
        cursor.execute(
            'SELECT {} '.format(', '.join(list(valid_columns.values())[0:-1])) + ', round((stock_actual - stock_reservado + stock_por_recibir),2) as stock_futuro, pedidos_reserva '
            'FROM articulo '
            'INNER JOIN categoria ON cod_categoria=id_categoria '
            'ORDER BY {} {}'.format(valid_columns[sort_column], sort_order)
            )
    else:
        # Execute the default query
        cursor.execute(
            'SELECT {} '.format(', '.join(list(valid_columns.values())[0:-1])) + ', round((stock_actual - stock_reservado + stock_por_recibir),2) as stock_futuro, pedidos_reserva '
            'FROM articulo '
            'INNER JOIN categoria ON cod_categoria=id_categoria '
            'ORDER BY stock_futuro ASC'
            )
    # Fetch all the rows from the query
    rows = cursor.fetchall()
    # Close the cursor and connection
    return render_template('articulos.html', rows=rows)


if __name__ == '__main__':
    app.run()

# update_order_data(7768)
# print(get_order_data(7768))

# articulos = GD.obtener_articulos()
# item = articulos[63]
# print(item)
# stock_reservado = item["stockDetail"][0]["totalReservedStock"]
# print(stock_reservado)