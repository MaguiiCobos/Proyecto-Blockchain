#comando para ejecutar (Magui :\ )
#python c:/Users/FLORENCIA/Desktop/Proyecto-Blockchain/back/app.py

#comando para ejecutar el reconocimiento facial
#C:\Users\flora\AppData\Local\Programs\Python\Python311\python.exe back/app.py
# python back/reconocer_usuario.py


from flask import Flask, request, jsonify, render_template, session
#from dotenv import load_dotenv
import os
import sys
import mysql.connector
from web3 import Web3
import subprocess

import tkinter as tk
from tkinter import messagebox


# from reconocer_usuario import capturar_y_reconocer
#from supabase import create_client

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import db_config  # Importás el diccionario

app = Flask(__name__, template_folder="../front/templates", static_folder="../front/static")

# Cargar variables de entorno desde el archivo .env
#load_dotenv()

# Cargar la clave secreta desde el archivo .env
app_secret_key = os.getenv('FLASK_SECRET_KEY')
app.secret_key = app_secret_key

# Configuración de la conexión a MariaDB
# db_config = {
#     'host': os.getenv('DB_HOST'),       # Cambia esto si tu base de datos está en otro servidor
#     'user': os.getenv('DB_USER'),       # Usuario de MariaDB
#     'password': os.getenv('DB_PASSWORD'),  # Contraseña de MariaDB
#     'database': os.getenv('DB_NAME'),        # Nombre de la base de datos
#     'port': os.getenv('DB_PORT')  # Cambia este valor si usas un puerto diferente
# }

# # Conexión a la red Ethereum (puedes usar Infura o Alchemy)
# infura_url = "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"
# web3 = Web3(Web3.HTTPProvider(infura_url))

# # Dirección del contrato y ABI
# contract_address = "0xYourContractAddress"
# contract_abi = [
#     # Copia aquí el ABI generado al compilar el contrato
# ]

# contract = web3.eth.contract(address=contract_address, abi=contract_abi)



@app.route('/verificar_dni', methods=['GET', 'POST'])
def verificar_dni():
    try:
        # Obtener el DNI desde la solicitud
        if request.method == 'GET':
            dni = request.args.get('dni')
        elif request.method == 'POST':
            data = request.get_json()
            dni = data.get('dni')

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Consultar si el votante existe y obtener si ya votó
        query = "SELECT ha_votado FROM votantes WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Evaluar resultados
        if resultado:
            if resultado['ha_votado'] == 0:
                session['voto_actual'] = {
                    'dni': dni,
                    'presidente': 0,
                    'gobernador': 0,
                    'intendente': 0
                }
                return jsonify({"existe": True, "habilitado": True, "mensaje": "DNI válido. Puede votar."})
            else:
                return jsonify({"existe": True, "habilitado": False, "mensaje": "Este votante ya ha votado."})
        else:
            return jsonify({"existe": False, "habilitado": False, "mensaje": "DNI no encontrado."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test_conexion', methods=['GET'])
def test_conexion():
    try:
        # Intentar conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Consulta simple para verificar la conexión
        cursor.fetchone()  # Lee el resultado de la consulta
        cursor.close()
        conn.close()
        return jsonify({"conexion": True, "mensaje": "Conexión exitosa a la base de datos"})
    except Exception as e:
        return jsonify({"conexion": False, "mensaje": f"Error en la conexión: {str(e)}"}), 500

@app.route('/registrar_voto', methods=['POST'])
#def registrar_voto():
    #try:
    #    data = request.get_json() #json = JavaScript Objet Notation
    #    dni = data['dni']
    #    vote_choice = data['vote_choice']
    #
    #    # Dirección del remitente (debe tener ETH para pagar el gas)
    #    sender_address = "0xYourWalletAddress"
    #    private_key = "YourPrivateKey"

        # Construir la transacción
    #    tx = contract.functions.registerVote(dni, vote_choice).buildTransaction({
    #        'from': sender_address,
    #        'nonce': web3.eth.getTransactionCount(sender_address),
    #        'gas': 2000000,
    #        'gasPrice': web3.toWei('50', 'gwei')
    #    })

        # Firmar y enviar la transacción
    #    signed_tx = web3.eth.account.signTransaction(tx, private_key)
    #    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #    return jsonify({"tx_hash": web3.toHex(tx_hash)})
    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500

@app.route('/ingresar_dni')
def ingresar_dni():
    return render_template('ingresar_dni.html')

@app.route('/como_votar')
def como_votar():
    return render_template('como_votar.html')

@app.route('/fin_voto')
def fin_voto():
    return render_template('fin_voto.html')

@app.route('/constancia')
def constancia():
    return render_template('constancia.html')

@app.route('/forma_voto')
def forma_voto():
    return render_template('forma_voto.html')

@app.route('/voto_blanco')
def voto_blanco():
    return render_template('voto_blanco.html')

@app.route('/tu_voto')
def tu_voto():
    # Conectar a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    candidatos = []

    # Obetener el presidente, gobernador e intendente del votante actual
    if 'voto_actual' in session :
        presidente = session['voto_actual']['presidente']
        gobernador = session['voto_actual']['gobernador']
        intendente = session['voto_actual']['intendente']

         # Diccionario para guardar IDs válidos de candidatos
        ids_candidatos = []

        # Función auxiliar para obtener ID si no es voto en blanco
        def obtener_id_candidato(query, id_partido, columna):
            if id_partido == 0:
                return None  # Voto en blanco
            cursor.execute(query, (id_partido,))
            resultado = cursor.fetchone()
            return resultado[columna] if resultado else None

        # Obtener IDs solo si no es voto en blanco
        id_presidente = obtener_id_candidato("SELECT id_presidente FROM partidos WHERE id_partidos = %s", presidente, 'id_presidente')
        id_gobernador = obtener_id_candidato("SELECT id_gobernador FROM partidos WHERE id_partidos = %s", gobernador, 'id_gobernador')
        id_intendente = obtener_id_candidato("SELECT id_intendente FROM partidos WHERE id_partidos = %s", intendente, 'id_intendente')

        # Crear lista con IDs válidos (no None)
        for id_c in [id_presidente, id_gobernador, id_intendente]:
            if id_c is not None:
                ids_candidatos.append(id_c)

        # Si hay algún candidato para consultar
        if ids_candidatos:
            query = f"SELECT * FROM candidatos WHERE id_candidato IN ({','.join(['%s'] * len(ids_candidatos))})"
            cursor.execute(query, ids_candidatos)
            candidatos = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        conn.close()

    return render_template('tu_voto.html', candidatos=candidatos)

@app.route('/reconocimiento')
def reconocimiento():
    return render_template('reconocimiento.html')

@app.route('/votacion')
def votacion():
    return render_template('votacion.html')

@app.route('/finalizar_votacion')
def finalizar_votacion():
    return render_template('finalizar_votacion.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

@app.route('/votacion_cat')
def votacion_cat():
    return render_template('votacion_cat.html')

# @app.route('/set_voto_test')
# def set_voto_test():
#     session['voto_actual'] = {
#         'presidente': 1,  # ID válido de partido
#         'gobernador': 0,  # voto en blanco
#         'intendente': 2   # otro ID de partido válido
#     }
#     return "Voto de prueba seteado en la sesión."

# @app.route('/ver_sesion')
# def ver_sesion():
#     if 'voto_actual' in session:
#         return jsonify({"sesion": session['voto_actual']})
#     return jsonify({"error": "No hay sesión activa"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)