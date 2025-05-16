#comando para ejecutar (Magui :\ )
#python c:/Users/FLORENCIA/Desktop/Proyecto-Blockchain/back/app.py


from flask import Flask, request, jsonify, render_template
import mysql.connector
from web3 import Web3

app = Flask(__name__, template_folder="../front/templates", static_folder="../front/static")

# Configuración de la conexión a MariaDB
db_config = {
    'host': 'localhost',       # Cambia esto si tu base de datos está en otro servidor
    'user': 'root',      # Usuario de MariaDB
    'password': '',  # Contraseña de MariaDB
    'database': 'blockchain',        # Nombre de la base de datos
    'port': 3306  # Cambia este valor si usas un puerto diferente
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

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Consultar si el DNI existe
        query = "SELECT COUNT(*) FROM votantes WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Verificar si el DNI existe
        if resultado[0] > 0:
            return jsonify({"existe": True, "mensaje": "DNI encontrado"})
        else:
            return jsonify({"existe": False, "mensaje": "DNI no encontrado"})
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
def registrar_voto():
    try:
        data = request.get_json()
        dni = data['dni']
        vote_choice = data['vote_choice']

        # Dirección del remitente (debe tener ETH para pagar el gas)
        sender_address = "0xYourWalletAddress"
        private_key = "YourPrivateKey"

        # Construir la transacción
        tx = contract.functions.registerVote(dni, vote_choice).buildTransaction({
            'from': sender_address,
            'nonce': web3.eth.getTransactionCount(sender_address),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        # Firmar y enviar la transacción
        signed_tx = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return jsonify({"tx_hash": web3.toHex(tx_hash)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/como_votar')
def como_votar():
    return render_template('como_votar.html')

@app.route('/fin_voto')
def fin_voto():
    return render_template('fin_voto.html')

@app.route('/constancia')
def constancia():
    return render_template('constancia.html')

@app.route('/ingresar_dni')
def ingresar_dni():
    return render_template('ingresar_dni.html')

@app.route('/reconocimiento')
def reconocimiento():
    return render_template('reconocimiento.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)



