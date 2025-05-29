import cv2  #Para procesamiento de imágenes
import face_recognition as fr  #Para reconocimiento facial, se instalo dlib para q funcione
import os # se instalo cdo se instalo python
import numpy as np  #Para manejo de arrays
from datetime import datetime # se instalo cdo se instalo python
import tkinter as tk # se instalo cdo se instalo python
from tkinter import simpledialog, messagebox
import time
import mysql.connector

from db_config import db_config  # Para usar la configuracion de la conexion (desde db_config.py)

#agregue 🔴

# Crear la ventana principal de tkinter
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

ruta = 'front/static/images/votantes'            
imagenes_votantes = []
nombres_votantes = []
lista_votantes = os.listdir(ruta)

# Carga los nombres de los votantes 
for nombre in lista_votantes:
    ruta_imagen = f"{ruta}/{nombre}"
    imagen_actual = cv2.imread(ruta_imagen)

    if imagen_actual is None:
        print(f"⚠️ No se pudo leer la imagen: {ruta_imagen}")
        continue  # Salta esta imagen si no se puede leer

    imagenes_votantes.append(imagen_actual)
    nombres_votantes.append(os.path.splitext(nombre)[0])


print(f"🔴 Lista de inscriptos para el evento: \n{nombres_votantes}")

# Codificar imagenes
def codificar(imagenes):
    lista_codificada = []
    for idx, imagen in enumerate(imagenes):
        try:
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            codificados = fr.face_encodings(imagen)
            if codificados:
                lista_codificada.append(codificados[0])
            else:
                print(f"⚠️ No se detectaron caras en la imagen {nombres_votantes[idx]}")
        except Exception as e:
            print(f"❌ Error al codificar una imagen: {str(e)}")
    return lista_codificada



# Abre la cámara y muestra video en tiempo real
def abrir_camara():
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        exito, frame = captura.read()
        cv2.imshow("Presiona 'c' para capturar la imagen", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            captura.release()
            cv2.destroyAllWindows()
            return frame


# Validar la imagen de usuario
def validar_imagenes():
    imagen = abrir_camara()    
    cara_captura = fr.face_locations(imagen)
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)
    
    if not cara_captura_codificada:
        messagebox.showerror("Error", "No se ha detectado ninguna cara en la imagen")
        validar_imagenes()
        return

    for cara_codif, cara_ubic in zip(cara_captura_codificada, cara_captura):
        distancias = fr.face_distance(lista_inscriptos_codificada, cara_codif)
        indice_coincidencia = np.argmin(distancias)
        
        if distancias[indice_coincidencia] > 0.6:
            messagebox.askyesno("Inscripción", "No estás en la lista de inscritos.")
        else:
            print(distancias[indice_coincidencia])
            nombre = nombres_votantes[indice_coincidencia]
            y1, x2, y2, x1 = cara_ubic
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            messagebox.showinfo("Acceso Permitido", f"Bienvenid@, {nombre}. Puedes ingresar a la reunión")
            cv2.imshow("Imagen capturada", imagen)
            cv2.waitKey(4000)  # Mostrar por 4 segundos
            cv2.destroyAllWindows()

lista_inscriptos_codificada = codificar(imagenes_votantes)

# Mensaje de bienvenida
messagebox.showinfo("Registro de voto", "Bienvenid@ al sistema de Votacion Electronico")
opcion = messagebox.askyesno("Registro", "¿Desea ingresar al Sistema de Votacion?")

if opcion:  # Si el usuario hace clic en "Sí"
    messagebox.showinfo("Validación", "Abriendo la cámara para capturar tu imagen")
    validar_imagenes()
else:
    messagebox.showinfo("Registro", "Has elegido no registrarte.")



'''

imagenes_votantes = []
nombres_votantes = []

# Ruta base donde están guardadas las imágenes
ruta_base = os.path.join("front", "static")


# Conectar a la base de datos
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor.execute("SELECT nombre, apellido, foto FROM blockchain.votantes")

for nombre, apellido, foto_relativa in cursor.fetchall():
    ruta_completa = os.path.join(ruta_base, *foto_relativa.split("/")[2:])  # quitar 'static/images/...' redundante
    if os.path.exists(ruta_completa):
        imagen = cv2.imread(ruta_completa)
        imagenes_votantes.append(imagen)
        nombres_votantes.append(f"{nombre} {apellido}")
        print(f"imagen de {nombre}:     {ruta_completa}")
    else:
        print(f"⚠️ No se encontró la imagen: {ruta_completa}")

cursor.close()
conn.close()

def codificar_imagenes(lista_imagenes):
    codificadas = []
    for i, imagen in enumerate(lista_imagenes):
        # Convertir imagen de BGR (OpenCV) a RGB (face_recognition)
        imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

        # Obtener codificación facial (embeddings)
        codificaciones = fr.face_encodings(imagen_rgb)

        if codificaciones:
            codificadas.append(codificaciones[0])  # Solo una cara por imagen esperada
        else:
            print(f"⚠️ No se encontró una cara en la imagen {i}. La imagen fue omitida.")

    return codificadas

# Usamos las imágenes que ya cargamos antes
codigos_rostros_votantes = codificar_imagenes(imagenes_votantes)

def capturar_y_reconocer(codigos_rostros_votantes, nombres_votantes):
    camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    votante_reconocido = None

    while True:
        ret, frame = camara.read()
        if not ret:
            break

        cv2.imshow("Presiona 'c' para capturar", frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            camara.release()
            cv2.destroyAllWindows()
            break

    # Procesar captura
    cara_ubicaciones = fr.face_locations(frame)
    codigos_capturados = fr.face_encodings(frame, cara_ubicaciones)

    if not codigos_capturados:
        messagebox.showerror("Error", "No se detectó ninguna cara.")
        return None

    # Solo tomamos la primera cara encontrada (una persona por vez)
    codigo_capturado = codigos_capturados[0]

    # Comparar con los codificados
    distancias = fr.face_distance(codigos_rostros_votantes, codigo_capturado)
    indice_match = np.argmin(distancias)

    if distancias[indice_match] > 0.6:
        messagebox.showwarning("Desconocido", "No estás registrado como votante.")
        return None
    else:
        nombre_reconocido = nombres_votantes[indice_match]
        messagebox.showinfo("Votante reconocido", f"Bienvenido/a, {nombre_reconocido}")
        return nombre_reconocido
'''
        




'''# Crear base de datos
ruta = './front/images/votantes'
mis_imagenes = []
nombres_inscriptos = []
lista_inscriptos = os.listdir(ruta)

# Carga los nombres de los inscriptos 
for nombre in lista_inscriptos:
    imagen_actual = cv2.imread(f"{ruta}/{nombre}")
    mis_imagenes.append(imagen_actual)
    nombres_inscriptos.append(os.path.splitext(nombre)[0])

print(f"Lista de inscriptos para el evento: \n{nombres_inscriptos}")

# Codificar imagenes
def codificar(imagenes):
    lista_codificada = []
    for imagen in imagenes:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        codificado = fr.face_encodings(imagen)[0]
        lista_codificada.append(codificado)
    return lista_codificada

# Registrar los ingresos
def registrar_ingresos(persona):
    f = open("registro.csv", "r+")
    lista_datos = f.readlines()
    nombres_registro = []

    for linea in lista_datos:
        ingreso = linea.split(',')
        nombres_registro.append(ingreso[0])

    if persona not in nombres_registro:
        ahora = datetime.now()
        str_ahora = ahora.strftime('%H:%M:%S')
        f.writelines(f"\n{persona}, {str_ahora}")

# Funciones agregada
def entregar_cronograma():
    f = open("cronograma.csv", "r+")
    lista_datos = f.readlines()
    messagebox.showinfo("Cronograma de la Reunión", lista_datos[1:])

# Registra un nuevo usuario
def registro(imagen):
    nombre_inscripto = simpledialog.askstring("Registro", "Ingrese su nombre y apellido:")
    if nombre_inscripto:
        ruta = f"Inscriptos/{nombre_inscripto}.jpg"
        cv2.imwrite(ruta, imagen)
        messagebox.showinfo("Registro", "Te has registrado con éxito")
    else:
        messagebox.showinfo("Registro", "Por favor ingrese su nombre y apellido")
        registro(imagen)

# Abre la cámara y muestra video en tiempo real
def abrir_camara():
    captura = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        exito, frame = captura.read()
        cv2.imshow("Presiona 'c' para capturar la imagen", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            captura.release()
            cv2.destroyAllWindows()
            return frame

# Validar la imagen de usuario
def validar_imagenes():
    imagen = abrir_camara()    
    cara_captura = fr.face_locations(imagen)
    cara_captura_codificada = fr.face_encodings(imagen, cara_captura)
    
    if not cara_captura_codificada:
        messagebox.showerror("Error", "No se ha detectado ninguna cara en la imagen")
        validar_imagenes()
        return

    for cara_codif, cara_ubic in zip(cara_captura_codificada, cara_captura):
        distancias = fr.face_distance(lista_inscriptos_codificada, cara_codif)
        indice_coincidencia = np.argmin(distancias)
        
        if distancias[indice_coincidencia] > 0.6:
            opcion = messagebox.askyesno("Inscripción", "No estás en la lista de inscritos. ¿Deseas registrarte?")
            if opcion:  # click en Sí
                registro(imagen)
            else:
                messagebox.showinfo("Registro", "Operación cancelada")
        else:
            print(distancias[indice_coincidencia])
            nombre = nombres_inscriptos[indice_coincidencia]
            entregar_cronograma()
            y1, x2, y2, x1 = cara_ubic
            cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(imagen, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(imagen, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            registrar_ingresos(nombre)
            messagebox.showinfo("Acceso Permitido", f"Bienvenid@, {nombre}. Puedes ingresar a la reunión")
            cv2.imshow("Imagen capturada", imagen)
            cv2.waitKey(4000)  # Mostrar por 4 segundos
            cv2.destroyAllWindows()

lista_inscriptos_codificada = codificar(mis_imagenes)

# Mensaje de bienvenida
messagebox.showinfo("Registro de Asistencia", "Bienvenid@ al sistema de registro de asistencias de evento")
opcion = messagebox.askyesno("Registro", "¿Desea ingresar al evento?")

if opcion:  # Si el usuario hace clic en "Sí"
    messagebox.showinfo("Validación", "Abriendo la cámara para capturar tu imagen")
    validar_imagenes()
else:
    messagebox.showinfo("Registro", "Has elegido no registrarte.")
'''