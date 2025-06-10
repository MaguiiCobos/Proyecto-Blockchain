#comando para ejecutar (Magui :\ )
#python c:/Users/FLORENCIA/Desktop/Proyecto-Blockchain/back/app.py

# <<<<<<< HEAD
# #comando para ejecutar el reconocimiento facia
# #C:\Users\flora\AppData\Local\Programs\Python\Python311\python.exe back/app.py
# # python back/reconocer_usuario.py


from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from dotenv import load_dotenv

# from flask import Flask, request, jsonify, render_template, session, redirect


from flask import Flask, request, jsonify, render_template, session, redirect, url_for
#from dotenv import load_dotenv
import os
import sys
import mysql.connector
from web3 import Web3
import subprocess

import tkinter as tk
from tkinter import messagebox
from blockchain.contrato import s_contrato, cuenta, w3  # Importar el contrato de votación

# Configuración para generar PDFs

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


from datetime import datetime
# from reconocer_usuario import capturar_y_reconocer
#from supabase import create_client

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_config import db_config

app = Flask(__name__, 
    template_folder="../front/templates",
    static_folder="../front/static"
)

# Clave secreta para las sesiones
app.secret_key = 'clave_secreta_temporal'

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
        if request.method == 'GET':
            dni = request.args.get('dni')
        elif request.method == 'POST':
            data = request.get_json()
            dni = data.get('dni')
        
        print(f"Verificando DNI: {dni}")

        if not dni:
            return jsonify({"existe": False, "habilitado": False, "mensaje": "DNI no proporcionado"}), 400

        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verificar si el DNI existe y obtener datos del votante
        query = "SELECT dni, nombre, apellido, ha_votado FROM votantes WHERE dni = %s"
        cursor.execute(query, (dni,))
        votante = cursor.fetchone()

        cursor.close()
        conn.close()

        if votante:
            if votante['ha_votado'] == 0:
                # Guardar datos del votante en la sesión
                session['voto_actual'] = {
                    'dni': dni,
                    'nombre': f"{votante['nombre']} {votante['apellido']}",
                    'presidente': 0,
                    'gobernador': 0,
                    'intendente': 0
                }
                print(f"Sesión creada para votante: {session['voto_actual']}")
                return jsonify({
                    "existe": True, 
                    "habilitado": True, 
                    "mensaje": "DNI válido. Puede proceder con el reconocimiento facial."
                })
            else:
                return jsonify({
                    "existe": True, 
                    "habilitado": False, 
                    "mensaje": "Este votante ya ha votado."
                })
        else:
            return jsonify({
                "existe": False, 
                "habilitado": False, 
                "mensaje": "DNI no encontrado en el padrón electoral."
            })

    except Exception as e:
        print(f"Error en verificar_dni: {str(e)}")
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
    try:
        # Verificar que la sesión existe y tiene los datos necesarios
        if 'voto_actual' not in session:
            return redirect(url_for('index'))
        
        # Verificar que todos los campos necesarios estén presentes
        required_fields = ['dni', 'presidente', 'gobernador', 'intendente']
        for field in required_fields:
            if field not in session['voto_actual']:
                session['voto_actual'][field] = 0  # Valor por defecto si falta algún campo
        
        # Obtener datos del votante
        dni = session['voto_actual']['dni']
        
        # Crear directorio para constancias si no existe
        constancias_dir = os.path.join('front', 'static', 'constancias')
        if not os.path.exists(constancias_dir):
            os.makedirs(constancias_dir)
        
        # Generar nombre único para el PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f'constancia_voto_{dni}_{timestamp}.pdf'
        pdf_path = os.path.join(constancias_dir, pdf_filename)
        
        # Crear el PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Estilo personalizado para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Estilo para el contenido
        content_style = ParagraphStyle(
            'CustomContent',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        # Agregar contenido al PDF
        story.append(Paragraph("CONSTANCIA DE VOTO", title_style))
        story.append(Spacer(1, 20))
        
        # Información del votante
        story.append(Paragraph(f"DNI del votante: {dni}", content_style))
        story.append(Paragraph(f"Fecha y hora de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", content_style))
        story.append(Spacer(1, 20))
        
        # Información de los votos
        votos = session['voto_actual']
        for cargo in ['presidente', 'gobernador', 'intendente']:
                story.append(Paragraph(f"{cargo.capitalize()}: Voto registrado", content_style))
        
        # Construir el PDF
        doc.build(story)
        
        # Guardar la ruta del PDF en la sesión para referencia
        session['constancia_pdf'] = pdf_filename
        
        return render_template('constancia.html')
        
    except Exception as e:
        print(f"Error al generar constancia: {str(e)}")
        return redirect(url_for('index'))

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

    votos = {
        'presidente': None,
        'gobernador': None,
        'intendente': None
    }

    # Obtener el presidente, gobernador e intendente del votante actual
    if 'voto_actual' in session:
        presidente = session['voto_actual']['presidente']
        gobernador = session['voto_actual']['gobernador']
        intendente = session['voto_actual']['intendente']

        # Función auxiliar para obtener información del partido y candidato
        def obtener_info_voto(id_partido, cargo):
            if id_partido == 0:
                return {'es_blanco': True}
            
            # Obtener información del partido y candidato
            query = """
                SELECT 
                    p.nombre as nombre_partido,
                    p.lista as lista,
                    p.foto_presidentes as foto_presidente,
                    p.foto_gobernadores as foto_gobernador,
                    p.foto_intendente as foto_intendente,
                    c.nombre,
                    c.apellido,
                    vc.nombre as nombre_vice,
                    vc.apellido as apellido_vice
                FROM partidos p
                LEFT JOIN candidatos c ON 
                    CASE 
                        WHEN %s = 'presidente' THEN p.id_presidente = c.id_candidato
                        WHEN %s = 'gobernador' THEN p.id_gobernador = c.id_candidato
                        WHEN %s = 'intendente' THEN p.id_intendente = c.id_candidato
                    END
                LEFT JOIN candidatos vc ON
                    CASE 
                        WHEN %s = 'presidente' THEN p.id_vice_presidente = vc.id_candidato
                        WHEN %s = 'gobernador' THEN p.id_vice_gobernador = vc.id_candidato
                        WHEN %s = 'intendente' THEN NULL
                    END
                WHERE p.id_partidos = %s
            """
            cursor.execute(query, (cargo, cargo, cargo, cargo, cargo, cargo, id_partido))
            resultado = cursor.fetchone()
            
            if resultado:
                foto = None
                if cargo == 'presidente':
                    foto = resultado['foto_presidente']
                elif cargo == 'gobernador':
                    foto = resultado['foto_gobernador']
                elif cargo == 'intendente':
                    foto = resultado['foto_intendente']

                return {
                    'es_blanco': False,
                    'partido': resultado['nombre_partido'],
                    'lista': resultado['lista'],
                    'candidato': f"{resultado['apellido']}, {resultado['nombre']}",
                    'vice': f"{resultado['apellido_vice']}, {resultado['nombre_vice']}" if resultado['nombre_vice'] else None,
                    'imagen': foto
                }
            return {'es_blanco': True}

        # Obtener información para cada cargo
        votos['presidente'] = obtener_info_voto(presidente, 'presidente')
        votos['gobernador'] = obtener_info_voto(gobernador, 'gobernador')
        votos['intendente'] = obtener_info_voto(intendente, 'intendente')

    # Cerrar la conexión
    cursor.close()
    conn.close()

    return render_template('tu_voto.html', votos=votos)

@app.route('/reconocimiento')
def reconocimiento():
    return render_template('reconocimiento.html')

@app.route('/votacion_comp')
def votacion():
    return render_template('votacion_comp.html')

@app.route('/finalizar_votacion')
def finalizar_votacion():
    return render_template('finalizar_votacion.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

@app.route('/votacion_cat')
def votacion_cat():
    return render_template('votacion_cat.html')


@app.route('/guardar_voto_template', methods=['POST'])
def guardar_voto_template():
    # Obtener los votos del formulario
    voto_presidente = request.form.get('voto_presidente')
    voto_gobernador = request.form.get('voto_gobernador')
    voto_intendente = request.form.get('voto_intendente')

    # Si el usuario no tiene sesión activa, redirigir
    if 'voto_actual' not in session:
        return "Sesión no encontrada. Por favor, vuelva a ingresar su DNI.", 400

    # Mapear los valores a IDs de partido (ajusta según tu lógica)
    def partido_a_id(valor):
        if valor == "CAMBIO":
            return 1
        elif valor == "VALOR":
            return 2
        elif valor == "UNIDOS":
            return 3
        elif valor == "BLANCO":
            return 99  # Usa el ID real del partido blanco
        return None

    id_presidente = partido_a_id(voto_presidente)
    id_gobernador = partido_a_id(voto_gobernador)
    id_intendente = partido_a_id(voto_intendente)

    # Actualizar la sesión
    session['voto_actual']['presidente'] = id_presidente
    session['voto_actual']['gobernador'] = id_gobernador
    session['voto_actual']['intendente'] = id_intendente

    return redirect('/tu_voto')

# @app.route('/set_voto_test')
# def set_voto_test():
#     session['voto_actual'] = {
#         'presidente': 1,  # ID válido de partido
#         'gobernador': 0,  # voto en blanco
#         'intendente': 2   # otro ID de partido válido
#     }
#     return "Voto de prueba seteado en la sesión."

@app.route('/set_voto_test')
def set_voto_test():
    session['voto_actual'] = {
        'presidente': 1,  # ID válido de partido
        'gobernador': 0,  # voto en blanco
        'intendente': 2   # otro ID de partido válido
    }
    return "Voto de prueba seteado en la sesión."


@app.route('/ver_sesion')
def ver_sesion():
    if 'voto_actual' in session:
        return jsonify({"sesion": session['voto_actual']})
    return jsonify({"error": "No hay sesión activa"}), 404

@app.route('/reconocer', methods=['POST'])
def reconocer():
    try:
        # Verificar que haya una sesión activa
        if 'voto_actual' not in session:
            return jsonify({
                "success": False, 
                "error": "No hay sesión de votación activa. Por favor, ingrese su DNI primero."
            }), 400

        # Obtener el DNI de la sesión
        dni = session['voto_actual'].get('dni')
        if not dni:
            return jsonify({
                "success": False, 
                "error": "DNI no encontrado en la sesión. Por favor, ingrese su DNI nuevamente."
            }), 400

        # Obtener la imagen del request
        data = request.get_json()
        if not data or 'imagen' not in data:
            return jsonify({
                "success": False, 
                "error": "No se recibió la imagen para el reconocimiento facial."
            }), 400

        # Importar y usar el procesador de imágenes
        from reconocer_usuario import procesar_imagen
        resultado = procesar_imagen(data['imagen'], dni)

        if resultado['success']:
            # Actualizar la sesión con el nombre reconocido
            session['voto_actual']['nombre_reconocido'] = resultado['nombre']
            print(f"Reconocimiento exitoso para DNI {dni}: {resultado['nombre']}")
        else:
            print(f"Error en reconocimiento para DNI {dni}: {resultado['error']}")

        return jsonify(resultado)

    except Exception as e:
        print(f"Error en el proceso de reconocimiento: {str(e)}")
        return jsonify({
            "success": False, 
            "error": f"Error en el proceso de reconocimiento: {str(e)}"
        }), 500

@app.route('/obtener_dni')
def obtener_dni():
    try:
        print("Obteniendo DNI de la sesión...")  # Log de inicio
        print(f"Contenido de la sesión: {session}")  # Log del contenido de la sesión
        
        if 'voto_actual' not in session:
            print("No hay sesión de votación activa")  # Log de error
            return jsonify({"error": "No hay sesión de votación activa"}), 400
            
        dni = session['voto_actual'].get('dni')
        print(f"DNI obtenido de la sesión: {dni}")  # Log del DNI
        
        if not dni:
            print("DNI no encontrado en la sesión")  # Log de error
            return jsonify({"error": "DNI no encontrado en la sesión"}), 400
            
        return jsonify({"dni": dni})
    except Exception as e:
        print(f"Error al obtener DNI: {str(e)}")  # Log de error
        return jsonify({"error": "Error al obtener el DNI"}), 500


@app.route('/guardar_voto')
def guardar_voto():
    if 'voto_actual' not in session:
        return "No hay voto en la sesión."

    voto = session['voto_actual']
    presidente = voto['presidente']
    gobernador = voto['gobernador']
    intendente = voto['intendente']    

    #Ejecutar la transacción
    try:
        #Guardar el voto en la blockchain
        tx_hash = s_contrato.functions.guardarVoto(presidente, gobernador, intendente).transact({'from': cuenta})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        #Obtener datos del bloque
        bloque = w3.eth.get_block(tx_receipt.blockNumber)
        timestamp = datetime.fromtimestamp(bloque.timestamp)

        #Guardar metadatos del voto en la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = """ 
            INSERT INTO transacciones_blockchain (tx_hash, bloque_numero, direccion_emisora, timestamp)
            VALUES(%s, %s, %s, %s)
                
        """
        
        values = (tx_hash.hex(), tx_receipt.blockNumber, cuenta, timestamp)
        
        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()



        return f"Voto guardado en la blockchain. Hash de transacción: {tx_hash.hex()}"
    except Exception as e:
        return f"Error al guardar el voto en la blockchain. {str(e)}"

@app.route('/ver_votos')
def ver_votos():
        
    try:
        total = s_contrato.functions.totalVotos().call()
        lista_votos = []

        for i in range(total):
            presidente, gobernador, intendente = s_contrato.functions.obtenerVoto(i).call()
            lista_votos.append({
                'presidente': presidente,
                'gobernador': gobernador,
                'intendente': intendente
            })
        

        #Obtener los metadatos de la BD
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) # dictionary=True para que devuelva cada fila como diccionario y no como tupla

        cursor.execute("SELECT * FROM transacciones_blockchain ORDER BY id ASC")
        transacciones = cursor.fetchall()

        cursor.close()
        conn.close()

        # Creo lista para poder mostrar todos los valores del bloque 
        votos_completos = []
        '''
        La función min en el bucle for se utiliza para encontrar el valor mínimo entre 
        las longitudes de las dos listas. 
        Esto significa que si lista_votos tiene 5 elementos y transacciones tiene 3, min devolverá 3.
        '''
        for i in range(min(len(lista_votos), len(transacciones))): 
            voto = lista_votos[i]
            meta = transacciones[i] #meta de metadato
            votos_completos.append({
                'presidente': voto['presidente'],
                'gobernador': voto['gobernador'],
                'intendente': voto['intendente'],
                'tx_hash': meta['tx_hash'],
                'bloque_numero': meta['bloque_numero'],
                'direccion_emisora': meta['direccion_emisora'],
                'timeStamp': meta['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            })

        return jsonify(votos_completos)
    
    except Exception as e:
        return f"Error al obtener los votos de la blockchain. {str(e)}"



if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    print(f"Directorio de templates: {app.template_folder}")
    print(f"Directorio de archivos estáticos: {app.static_folder}")
    print("La aplicación Flask se ejecutará en el puerto 5000")
    print("La base de datos MySQL se conectará en el puerto 3306")
    app.run(debug=True, port=5000, host='127.0.0.1')