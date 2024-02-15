from app import app
from funciones.controllers1 import datos_del_cliente
from funciones.controllers1 import data_clientes
from flask import request



@app.route('/api/datos_boletas', methods=['POST'])
def data_cliente():
    data = data_clientes()
    return data


@app.route('/api/all_data', methods=['POST'])
def get_data():
    data = datos_del_cliente()
    return data
