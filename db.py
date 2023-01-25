import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to the MySQL database using the connection details from the .env file
cnx = mysql.connector.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'),
                              host=os.getenv('MYSQL_HOST'), database=os.getenv('MYSQL_DB'))
cursor = cnx.cursor()

def cargar_articulos(item):
    id_articulo = int(item["code"])
    nombre = item["name"]
    unidad_venta = item["unit"]
    if type(item["categoryID"]) == int:
        cod_categoria = int(item["categoryID"])
    else:
        cod_categoria = 0
    stock_actual = item["stock"]
    try:
        stock_reservado = item["stockDetail"][0]["totalReservedStock"]
    except:
        stock_reservado = 0
    # Insert the values into the database
    pedidos_reserva = []
    for pedido in item["reservedStock"]:
        pedidos_reserva.append(str(pedido["orderNumber"]))
    if pedidos_reserva:
        pedidos_reserva = ", ".join(pedidos_reserva)
    else:
        pedidos_reserva = ""
    try:
        cursor.execute(
        'INSERT INTO articulo (id_articulo,nombre,unidad_venta,cod_categoria,stock_actual,stock_reservado, pedidos_reserva) '
        f'VALUES ({id_articulo},"{nombre}","{unidad_venta}",{cod_categoria},{stock_actual},{stock_reservado}, "{pedidos_reserva}") as a '
        'ON DUPLICATE KEY UPDATE nombre=a.nombre,unidad_venta=a.unidad_venta,cod_categoria=a.cod_categoria,'
        'stock_actual=a.stock_actual,stock_reservado=a.stock_reservado, pedidos_reserva=a.pedidos_reserva')
    except Exception as e:
        print("Error al cargar artículo ",id_articulo, e)
    # Commit the changes to the database
    cnx.commit()

def cargar_categorias(item):
    id_categoria = item["categoryID"]
    nombre_categoria = item["description"]
    cursor.execute(
        'INSERT INTO categoria (id_categoria,nombre_categoria) '
        f'VALUES ({id_categoria},"{nombre_categoria}") as c '
        'ON DUPLICATE KEY UPDATE nombre_categoria=c.nombre_categoria')
    cnx.commit()

def cargar_orden_compra(item):
    id_oc = item["purchaseOrderData"]["number"]
    linea = item[""]
    cod_articulo = item[""]
    cantidad_oc = item[""]
    precio_oc = item[""]
    fecha_oc = item[""]
    id_proveedor = item[""]
    cursor.execute(
        'INSERT INTO orden_compra (id_oc, linea, cod_articulo, cantidad_oc, precio_oc, fecha_oc, id_proveedor) '
        f'VALUES ({id_oc}, {linea}, {cod_articulo}, {cantidad_oc}, {precio_oc}, {fecha_oc}, "{id_proveedor}") as oc '
        'ON DUPLICATE KEY UPDATE id_oc=oc.id_oc, linea=oc.linea, cod_articulo=oc.cod_articulo, '
        'cantidad_oc=oc.cantidad_oc, precio_oc=oc.precio_oc, fecha_oc=oc.fecha_oc, id_proveedor=oc.id_proveedor')
    cnx.commit()

def cargar_stock_futuro(item):
    id_articulo = int(item["productCode"])
    stock_por_recibir = int(item["stockToReceive"])
    # Insert the values into the database
    try:
        cursor.execute(
        'INSERT INTO articulo (id_articulo,stock_por_recibir) '
        f'VALUES ({id_articulo},{stock_por_recibir}) as a '
        'ON DUPLICATE KEY UPDATE stock_por_recibir=a.stock_por_recibir')
    except Exception as e:
        print("Error al cargar stock por recibir artículo ",id_articulo, " (stock futuro)", e)
    # Commit the changes to the database
    cnx.commit()