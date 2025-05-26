#comando para ejecutar (Magui :\ )
#python c:/Users/FLORENCIA/Desktop/Proyecto-Blockchain/back/app.py


from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
import os
import mysql.connector
from web3 import Web3

app = Flask(__name__, template_folder="../front/templates", static_folder="../front/static")

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Cargar la clave secreta desde el archivo .env
app_secret_key = os.getenv('FLASK_SECRET_KEY')

# Configuración de la conexión a MariaDB
db_config = {
    'host': os.getenv('DB_HOST'),       # Cambia esto si tu base de datos está en otro servidor
    'user': os.getenv('DB_USER'),       # Usuario de MariaDB
    'password': os.getenv('DB_PASSWORD'),  # Contraseña de MariaDB
    'database': os.getenv('DB_NAME'),        # Nombre de la base de datos
    'port': os.getenv('DB_PORT')  # Cambia este valor si usas un puerto diferente
}

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
            dni = request.args.get('dni')  # Para solicitudes GET
        elif request.method == 'POST':
            data = request.get_json()
            dni = data.get('dni')  # Para solicitudes POST

#         # Conectar a la base de datos
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()

#         # Consultar si el DNI existe
#         query = "SELECT COUNT(*) FROM votantes WHERE dni = %s"
#         cursor.execute(query, (dni,))
#         resultado = cursor.fetchone()

#         # Cerrar la conexión
#         cursor.close()
#         conn.close()

        # Verificar si el DNI existe
        if resultado[0] > 0:
            session['voto_actual'] = {
                'dni': dni,
                'presidente': 0,
                'gobernador': 0,
                'intendente': 0
            }
            return jsonify({"existe": True, "mensaje": "DNI encontrado"})
        else:
            return jsonify({"existe": False, "mensaje": "DNI no encontrado"})

        # Si se encontró el DNI
        ha_votado = resultado[0]
        return jsonify({
            "existe": True,
            "ha_votado": ha_votado,
            "mensaje": "DNI encontrado"
        })

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
   # try:
    #     data = request.get_json() #json = JavaScript Objet Notation
    #     dni = data['dni']
    #     vote_choice = data['vote_choice']

    #     # Dirección del remitente (debe tener ETH para pagar el gas)
    #     sender_address = "0xYourWalletAddress"
    #     private_key = "YourPrivateKey"

    #     # Construir la transacción
    #     tx = contract.functions.registerVote(dni, vote_choice).buildTransaction({
    #         'from': sender_address,
    #         'nonce': web3.eth.getTransactionCount(sender_address),
    #         'gas': 2000000,
    #         'gasPrice': web3.toWei('50', 'gwei')
    #     })

    #     # Firmar y enviar la transacción
    #     signed_tx = web3.eth.account.signTransaction(tx, private_key)
    #     tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #     return jsonify({"tx_hash": web3.toHex(tx_hash)})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

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
    return render_template('tu_voto.html')

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



if __name__ == '__main__':
    app.run(debug=True, port=5000)