import requests

res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
# print(type(res))
# print(res.status_code == requests.codes.ok)
# print(print(res.text[:250]))


valid_columns = {
    '0': 'id_articulo',
    '1': 'nombre',
    '2': 'unidad_venta',
    '3': 'nombre_categoria',
    '4': 'stock_actual',
    '5': 'stock_reservado',
    '6': 'stock_futuro'
    }
# print('SELECT {} '.format(', '.join(list(valid_columns.values())[0:-1])) + ', (stock_actual - stock_reservado) as stock_futuro, pedidos_reserva ')
lista_vacia = []

if lista_vacia:
    print("Hola")