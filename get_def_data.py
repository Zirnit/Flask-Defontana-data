import requests, datetime, os, json
from math import ceil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# HTTP headers to use when making API requests
dKey = os.getenv('dKey')
headers = {"Authorization": dKey}
hoy = datetime.date.today()
hace1Semana = hoy - datetime.timedelta(days=7)
en1Semana = hoy + datetime.timedelta(days=7)

def get_def_data():
    api_url = "https://api.defontana.com/api/Order/List"
    
    querystring = {
        "FromDate":hace1Semana,
        "ToDate":en1Semana,
        "ItemsPerPage":"1000",
        "PageNumber":"0",
        "fromNumber":"4400"
        }
    response = requests.request("GET", api_url, headers=headers, params=querystring).json()
    return response

def get_order_data(order_number):
    api_url = f"https://api.defontana.com/api/Order/Get"
    querystring = {"number":order_number}
    response = requests.get(api_url, headers=headers, params=querystring).json()
    return response

def obtener_articulos():
    url = "https://api.defontana.com/api/Sale/Getproducts"
    itemspp = 250
    data = "productList"
    dict_pagenumber = "pageNumber"
    querystring = {"status":"1","itemsPerPage":itemspp,"pageNumber":"1"}
    num_paginas = obtener_n_paginas(url, querystring)
    listaJson = obtener_datos_paginados(url, itemspp, num_paginas, querystring, data, dict_pagenumber)
    return listaJson

def obtener_categorías():
    url = "https://api.defontana.com/api/Sale/GetCategories"
    querystring = {"itemsPerPage":"100","pageNumber":"1"}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response['categoriesList']

def obtener_lista_ordenes_compra():
    url = "https://api.defontana.com/api/PurchaseOrder/List"
    itemspp = 100
    data = "data"
    dict_pagenumber = "Page"
    querystring = {
        "FromDate" : "2022-01-01",
        "ToDate" : hoy,
        "ItemsPerPage": "10",
        "Page" : "0",
        "Status" : 0
    }
    num_paginas = obtener_n_paginas(url, querystring)
    listaJson = obtener_datos_paginados(url, itemspp, num_paginas, querystring, data, dict_pagenumber)
    lista_OC = []
    for item in listaJson:
        lista_OC.append(obtener_ordenes_compra(item["number"]))
    return lista_OC

def obtener_ordenes_compra(number):
    url = "https://api.defontana.com/api/PurchaseOrder/Get"
    querystring = {"Number" : number}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response

def obtener_stock_futuro():
    url = "https://api.defontana.com/api/Inventory/GetFutureStockInfo"
    itemspp = 250
    querystring = {"ItemsPerPage":itemspp,"Page":"1"}
    num_paginas = obtener_n_paginas(url,querystring)
    data = "productsDetail"
    dict_pagenumber="Page"
    listaJson = obtener_datos_paginados(url,itemspp,num_paginas,querystring,data,dict_pagenumber)
    return listaJson

def obtener_proveedores():
    url = "https://api.defontana.com/api/PurchaseOrder/GetProviders"
    itemspp = 250
    dict_pagenumber = "pageNumber"
    querystring = {"status":"0","itemsPerPage":itemspp,dict_pagenumber:1}
    data = "providersList"
    num_paginas = obtener_n_paginas(url, querystring)
    return obtener_datos_paginados(url, itemspp, num_paginas, querystring, data, dict_pagenumber)

def obtener_datos_paginados(url, itemspp, num_paginas, querystring, data, dict_pagenumber):
    todas_las_respuestas = ["["]
    for i in range(1, num_paginas+1):
        querystring = {"status":"0","itemsPerPage":itemspp,dict_pagenumber:i}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response.raise_for_status()
        respuesta = json.loads(response.text)[data]
        for r in respuesta:
            if "address" in r and r["address"]:
                if '"' in r["address"]:
                    r["address"] = str(r["address"]).replace('"',"")
                if "'" in r["address"]:
                    r["address"] = str(r["address"]).replace("'","")
            todas_las_respuestas.append(str(r))
            todas_las_respuestas.append(",")
    listaAux = "".join(todas_las_respuestas)
    listaAux = listaAux.replace(r"\xa0", "")
    listaAux = listaAux.replace("\\","")
    listaAux = listaAux.replace("None", "'None'")
    listaAux = listaAux.replace("False","'False'")
    listaAux = listaAux.replace("True","'True'")
    listaAux = listaAux.replace("'","\"")
    listaAux = listaAux[:-2] + "}]"
    listaJson = json.loads(listaAux)
    return listaJson

def obtener_n_paginas(url, querystring):
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    response = response.json()
    num_paginas = ceil(response["totalItems"]/response["itemsPerPage"])
    return num_paginas
