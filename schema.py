instructions = [
        "SET FOREIGN_KEY_CHECKS=0;",
        "DROP TABLE IF EXISTS articulo",
        "DROP TABLE IF EXISTS categoria",
        "DROP TABLE IF EXISTS compra",
        "DROP TABLE IF EXISTS proveedor",
        "DROP TABLE IF EXISTS orden_compra",
        "SET FOREIGN_KEY_CHECKS=1;",
        """
        create table articulo (
        id_articulo int primary key, 
        nombre varchar(250),
        unidad_venta varchar(250),
        cod_categoria int,
        stock_actual float,
        stock_reservado float,
        pedidos_reserva varchar(250),
        stock_por_recibir int
        )
        """,
        """
        create table categoria (
        id_categoria int primary key,
        nombre_categoria varchar(250) not null
        )
        """,
        """
        create table compra (
        id_compra int primary key,
        num_parte_entrada int,
        fecha_compra date not null,
        id_proveedor varchar(250) not null,
        cod_articulo int not null,
        cantidad_compra float not null,
        precio_compra int not null
        )
        """,
        """
        create table proveedor (
        id_proveedor varchar(250) primary key,
        nombre_prov varchar(250) not null,
        direccion_prov varchar(250),
        contacto_prov varchar(250),
        telefono_prov varchar(250)
        )
        """,
        """
        create table orden_compra (
        id int primary key auto_increment,
        id_oc int not null,
        linea int,
        cod_articulo int not null,
        cantidad_oc float not null,
        precio_oc int not null,
        fecha_oc date not null,
        id_proveedor varchar(250) not null
        )
        """
]