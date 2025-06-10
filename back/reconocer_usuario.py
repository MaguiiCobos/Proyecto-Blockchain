import cv2  #Para procesamiento de imágenes
import face_recognition as fr  #Para reconocimiento facial, se instalo dlib para q funcione
import os # se instalo cdo se instalo python
import numpy as np  #Para manejo de arrays
from datetime import datetime # se instalo cdo se instalo python
import tkinter as tk # se instalo cdo se instalo python
from tkinter import simpledialog, messagebox
import time
import mysql.connector
import base64
from PIL import Image
import io

from db_config import db_config  # Para usar la configuracion de la conexion (desde db_config.py)

# Crear la ventana principal de tkinter
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

ruta = 'front/static/images/votantes'            
imagenes_votantes = []
nombres_votantes = []
lista_votantes = os.listdir(ruta)

def asegurar_formato_imagen(ruta_imagen):
    """Asegura que la imagen esté en formato RGB de 8 bits o escala de grises"""
    try:
        # Abrir la imagen con PIL
        with Image.open(ruta_imagen) as img:
            # Convertir a RGB si no lo es
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si es necesario
            max_size = 800
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convertir a array numpy y asegurar que sea uint8
            img_array = np.array(img, dtype=np.uint8)
            
            # Verificar y corregir el formato
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                # Ya está en RGB
                print(f"Imagen en formato RGB: shape={img_array.shape}, dtype={img_array.dtype}")
            else:
                # Convertir a escala de grises
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                print(f"Imagen convertida a escala de grises: shape={img_array.shape}, dtype={img_array.dtype}")
            
            return img_array
    except Exception as e:
        print(f"Error al procesar imagen {ruta_imagen}: {str(e)}")
        return None

# Carga los nombres de los votantes 
print("\n=== Iniciando carga de votantes ===")
for nombre in lista_votantes:
    ruta_imagen = f"{ruta}/{nombre}"
    try:
        # Procesar la imagen para asegurar formato correcto
        imagen = asegurar_formato_imagen(ruta_imagen)
        if imagen is None:
            print(f"Error: No se pudo procesar la imagen: {ruta_imagen}")
            continue
        
        imagenes_votantes.append(imagen)
        nombres_votantes.append(os.path.splitext(nombre)[0])
        print(f"Imagen cargada correctamente: {nombre} (tamaño: {imagen.shape}, tipo: {imagen.dtype})")
    except Exception as e:
        print(f"Error al cargar la imagen {nombre}: {str(e)}")
        continue

print("\nLista de votantes cargados:")
for nombre in nombres_votantes:
    print(f"- {nombre}")

# Codificar imagenes
def codificar(imagenes):
    lista_codificada = []
    for idx, imagen in enumerate(imagenes):
        try:
            print(f"\nProcesando imagen de {nombres_votantes[idx]}")
            print(f"Formato original: shape={imagen.shape}, dtype={imagen.dtype}")
            
            # Convertir a formato correcto usando PIL
            try:
                # Convertir a PIL Image
                pil_image = Image.fromarray(imagen)
                
                # Convertir a RGB si no lo es
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
                
                # Convertir de vuelta a numpy array
                imagen = np.array(pil_image, dtype=np.uint8)
                
                # Verificar y corregir el formato
                if len(imagen.shape) == 3 and imagen.shape[2] == 3:
                    # Ya está en RGB
                    print("Imagen en formato RGB correcto")
                else:
                    # Convertir a escala de grises
                    imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
                    print("Imagen convertida a escala de grises")
                
                print(f"Formato final: shape={imagen.shape}, dtype={imagen.dtype}")
            except Exception as e:
                print(f"Error al convertir formato: {str(e)}")
                continue
            
            # Verificar si la imagen está vacía o corrupta
            if imagen is None or imagen.size == 0:
                print("Error: La imagen está vacía o corrupta")
                continue
            
            # Verificar valores de píxeles
            print(f"Rango de valores de píxeles: min={imagen.min()}, max={imagen.max()}")
            
            # Intentar codificar
            print("Intentando codificar el rostro...")
            try:
                # Primero detectar las caras
                face_locations = fr.face_locations(imagen)
                if not face_locations:
                    print(f"No se detectaron caras en la imagen {nombres_votantes[idx]}")
                    continue
                
                print(f"Se detectaron {len(face_locations)} caras")
                codificados = fr.face_encodings(imagen, face_locations)
                
                if codificados:
                    lista_codificada.append(codificados[0])
                    print(f"Imagen {nombres_votantes[idx]} codificada correctamente")
                else:
                    print(f"No se pudieron codificar las caras detectadas en {nombres_votantes[idx]}")
            except Exception as e:
                print(f"Error específico en face_encodings: {str(e)}")
                raise
                
        except Exception as e:
            print(f"Error al codificar la imagen {nombres_votantes[idx]}: {str(e)}")
            print(f"Formato de la imagen: shape={imagen.shape}, dtype={imagen.dtype}")
            # Intentar cargar la imagen directamente con face_recognition
            try:
                print("Intentando cargar la imagen directamente con face_recognition...")
                imagen_directa = asegurar_formato_imagen(f"{ruta}/{nombres_votantes[idx]}.jpg")
                if imagen_directa is not None:
                    # Intentar detectar caras primero
                    face_locations = fr.face_locations(imagen_directa)
                    if not face_locations:
                        print(f"No se detectaron caras en la imagen {nombres_votantes[idx]} (método alternativo)")
                        continue
                    
                    print(f"Se detectaron {len(face_locations)} caras (método alternativo)")
                    codificados = fr.face_encodings(imagen_directa, face_locations)
                    if codificados:
                        lista_codificada.append(codificados[0])
                        print(f"Imagen {nombres_votantes[idx]} codificada correctamente (método alternativo)")
                    else:
                        print(f"No se pudieron codificar las caras detectadas en {nombres_votantes[idx]} (método alternativo)")
                else:
                    print(f"No se pudo cargar la imagen {nombres_votantes[idx]} (método alternativo)")
            except Exception as e2:
                print(f"Error en método alternativo: {str(e2)}")
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
        print("No se ha detectado ninguna cara en la imagen")
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
            # messagebox.showinfo("Acceso Permitido", f"Bienvenid@, {nombre}. Puedes ingresar a la reunión")
            cv2.imshow("Imagen capturada", imagen)
            cv2.waitKey(4000)  # Mostrar por 4 segundos
            cv2.destroyAllWindows()

lista_inscriptos_codificada = codificar(imagenes_votantes)

# Mensaje de bienvenida
# messagebox.showinfo("Registro de voto", "Bienvenid@ al sistema de Votacion Electronico")
# opcion = messagebox.askyesno("Registro", "¿Desea ingresar al Sistema de Votacion?")

# if opcion:  # Si el usuario hace clic en "Sí"
#     messagebox.showinfo("Validación", "Abriendo la cámara para capturar tu imagen")
#     validar_imagenes()
# else:
#     messagebox.showinfo("Registro", "Has elegido no registrarte.")



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

class ReconocimientoFacial:
    def __init__(self):
        self.rostros_votantes = {}
        self.umbral_similitud = 0.6

    def cargar_votantes(self):
        """Carga las imágenes de los votantes desde la base de datos"""
        try:
            print("\n=== Iniciando carga de votantes ===")
            
            # Verificar que exista el directorio de imágenes
            ruta_base = os.path.join("front", "static", "images", "votantes")
            if not os.path.exists(ruta_base):
                print(f"ERROR: El directorio de imágenes no existe: {ruta_base}")
                raise Exception(f"El directorio de imágenes no existe: {ruta_base}")
            
            print(f"Directorio de imágenes encontrado: {ruta_base}")
            print("Imágenes disponibles:")
            for archivo in os.listdir(ruta_base):
                print(f"- {archivo}")
            
            # Conectar a la base de datos
            print("\nConectando a la base de datos...")
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Obtener los votantes con sus imágenes
            print("\nConsultando votantes con imágenes...")
            cursor.execute("""
                SELECT dni, nombre, apellido, foto, nombre_foto 
                FROM votantes 
                WHERE foto IS NOT NULL AND foto != ''
            """)
            
            votantes = cursor.fetchall()
            print(f"Se encontraron {len(votantes)} votantes con imágenes en la base de datos")
            
            if len(votantes) == 0:
                print("\nNo se encontraron votantes con imágenes en la base de datos")
                raise Exception("No se encontraron votantes con imágenes en la base de datos")
            
            # Procesar cada votante
            for dni, nombre, apellido, foto_relativa, nombre_foto in votantes:
                try:
                    print(f"\nProcesando votante: DNI={dni}, Nombre={nombre} {apellido}, Nombre foto: {nombre_foto}")
                    
                    # Construir la ruta de la imagen usando el DNI
                    ruta_completa = os.path.join(ruta_base, f"{nombre_foto}.jpg")
                    print(f"😘Buscando imagen en: {ruta_completa}")
                    
                    if not os.path.exists(ruta_completa):
                        print(f"ERROR: No se encontró la imagen para DNI {dni}")
                        continue
                    
                    # Cargar la imagen con OpenCV (esto devuelve BGR)
                    imagen_bgr = cv2.imread(ruta_completa)
                    if imagen_bgr is None:
                        print(f"ERROR: No se pudo leer la imagen: {ruta_completa}")
                        continue
                    
                    # Redimensionar si es necesario
                    if max(imagen_bgr.shape) > 800:
                        scale = 800 / max(imagen_bgr.shape)
                        new_shape = tuple(int(dim * scale) for dim in imagen_bgr.shape[:2])
                        imagen_bgr = cv2.resize(imagen_bgr, (new_shape[1], new_shape[0]))
                        print(f"Imagen redimensionada a: {new_shape}")
                    
                    # Convertir BGR a RGB (necesario para face_recognition)
                    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
                    print(f"Imagen convertida a RGB: shape={imagen_rgb.shape}, dtype={imagen_rgb.dtype}")
                    
                    # Detectar y codificar el rostro
                    ubicaciones = fr.face_locations(imagen_rgb)
                    if ubicaciones:
                        print(f"Se detectaron {len(ubicaciones)} rostros")
                        codificaciones = fr.face_encodings(imagen_rgb, ubicaciones)
                        if codificaciones:
                            # Guardar las codificaciones del rostro
                            if dni not in self.rostros_votantes:
                                self.rostros_votantes[dni] = []
                            self.rostros_votantes[dni].extend(codificaciones)
                            print(f"Imagen procesada correctamente para DNI: {dni}")
                        else:
                            print(f"No se pudo codificar el rostro para DNI: {dni}")
                    else:
                        print(f"No se detectó ningún rostro para DNI: {dni}")
                    
                except Exception as e:
                    print(f"Error al procesar votante DNI {dni}: {str(e)}")
                    continue
            
            cursor.close()
            conn.close()
            
            # Verificar si se cargaron imágenes correctamente
            if not self.rostros_votantes:
                print("\nERROR: No se pudo cargar ninguna imagen de votante correctamente")
                print("Resumen de errores:")
                print("1. Verificar que las imágenes existan en:", ruta_base)
                print("2. Verificar que los nombres de las imágenes coincidan con los DNIs")
                print("3. Verificar que las imágenes contengan rostros detectables")
                raise Exception("No se pudo cargar ninguna imagen de votante correctamente")
            
            print(f"\nResumen: Se cargaron correctamente {len(self.rostros_votantes)} votantes")
            print("DNIs cargados:", list(self.rostros_votantes.keys()))
            
        except Exception as e:
            print(f"\nError al cargar votantes: {str(e)}")
            raise

    def procesar_imagen_base64(self, imagen_base64):
        """Convierte una imagen base64 a formato OpenCV"""
        try:
            print("\n=== Iniciando procesamiento de imagen base64 ===")
            
            # Eliminar el prefijo de la cadena base64 si existe
            if ',' in imagen_base64:
                imagen_base64 = imagen_base64.split(',')[1]
            
            # Decodificar la imagen base64
            imagen_bytes = base64.b64decode(imagen_base64)
            
            # Convertir bytes a array numpy
            nparr = np.frombuffer(imagen_bytes, np.uint8)
            
            # Decodificar la imagen con OpenCV (esto devuelve BGR)
            imagen_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if imagen_bgr is None:
                raise ValueError("No se pudo decodificar la imagen")
            
            print(f"Imagen decodificada: shape={imagen_bgr.shape}, dtype={imagen_bgr.dtype}")
            
            # Convertir BGR a RGB (necesario para face_recognition)
            imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
            print(f"Imagen convertida a RGB: shape={imagen_rgb.shape}, dtype={imagen_rgb.dtype}")
            return imagen_rgb
            
        except Exception as e:
            print(f"Error al procesar imagen base64: {str(e)}")
            raise

    def reconocer_rostro(self, imagen):
        """Reconoce un rostro en la imagen y lo compara con los votantes registrados"""
        try:
            print("\n=== Iniciando reconocimiento facial ===")
            print(f"Dimensiones de la imagen: {imagen.shape}")
            
            # Detectar rostros en la imagen
            print("Detectando rostros...")
            ubicaciones = fr.face_locations(imagen)
            if not ubicaciones:
                print("No se detectó ningún rostro en la imagen")
                return None, "No se detectó ningún rostro en la imagen"
            
            print(f"Se detectaron {len(ubicaciones)} rostros")
            
            # Codificar el rostro detectado
            print("Codificando rostro detectado...")
            codificaciones = fr.face_encodings(imagen, ubicaciones)
            if not codificaciones:
                print("No se pudo codificar el rostro detectado")
                return None, "No se pudo codificar el rostro detectado"
            
            print("Comparando con rostros registrados...")
            # Variables para guardar la mejor coincidencia
            mejor_distancia = float('inf')
            mejor_dni = None
            
            # Comparar con los rostros registrados
            for codificacion in codificaciones:
                for dni, rostros_registrados in self.rostros_votantes.items():
                    print(f"\nComparando con votante DNI: {dni}")
                    for rostro_registrado in rostros_registrados:
                        # Calcular la distancia entre los rostros
                        distancia = fr.face_distance([rostro_registrado], codificacion)[0]
                        print(f"Distancia: {distancia}")
                        
                        # Si la distancia es menor al umbral y es la mejor hasta ahora
                        if distancia < self.umbral_similitud and distancia < mejor_distancia:
                            mejor_distancia = distancia
                            mejor_dni = dni
                            print(f"Nueva mejor coincidencia encontrada! DNI: {dni}, Distancia: {distancia}")
            
            # Verificar si se encontró alguna coincidencia válida
            if mejor_dni is not None:
                print(f"\nMejor coincidencia encontrada:")
                print(f"DNI: {mejor_dni}")
                print(f"Distancia: {mejor_distancia}")
                return mejor_dni, None
            else:
                print("\nNo se encontró ninguna coincidencia válida")
                return None, "No se encontró ninguna coincidencia válida"
                
        except Exception as e:
            print(f"Error en el reconocimiento facial: {str(e)}")
            return None, str(e)

def procesar_imagen(imagen_base64, dni):
    """Función principal para procesar una imagen y reconocer al votante"""
    try:
        print(f"\n=== Iniciando procesamiento de imagen para DNI: {dni} ===")
        print("1. Verificando conexión a la base de datos...")
        
        # Crear instancia del reconocedor
        reconocedor = ReconocimientoFacial()
        
        # Cargar votantes
        print("\n2. Cargando votantes desde la base de datos...")
        try:
            reconocedor.cargar_votantes()
        except Exception as e:
            print(f"Error al cargar votantes: {str(e)}")
            print("Verificando directorio de imágenes...")
            ruta_imagenes = os.path.join("front", "static", "images", "votantes")
            if os.path.exists(ruta_imagenes):
                print(f"Contenido del directorio {ruta_imagenes}:")
                for archivo in os.listdir(ruta_imagenes):
                    print(f"- {archivo}")
            else:
                print(f"El directorio {ruta_imagenes} no existe")
            raise
        
        # Procesar la imagen base64
        print("\n3. Procesando imagen base64...")
        try:
            # Eliminar el prefijo de la cadena base64 si existe
            if ',' in imagen_base64:
                imagen_base64 = imagen_base64.split(',')[1]
            
            # Decodificar la imagen base64
            imagen_bytes = base64.b64decode(imagen_base64)
            
            # Convertir bytes a array numpy
            nparr = np.frombuffer(imagen_bytes, np.uint8)
            
            # Decodificar la imagen con OpenCV (esto devuelve BGR)
            imagen_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if imagen_bgr is None:
                raise ValueError("No se pudo decodificar la imagen")
            
            print(f"Imagen decodificada: shape={imagen_bgr.shape}, dtype={imagen_bgr.dtype}")
            
            # Convertir BGR a RGB (necesario para face_recognition)
            imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
            print(f"Imagen convertida a RGB: shape={imagen_rgb.shape}, dtype={imagen_rgb.dtype}")
            
        except Exception as e:
            print(f"Error al procesar imagen base64: {str(e)}")
            raise
        
        # Reconocer el rostro
        print("\n4. Intentando reconocer el rostro...")
        try:
            dni_reconocido, error = reconocedor.reconocer_rostro(imagen_rgb)
            if error:
                print(f"Error en el reconocimiento: {error}")
                return {"success": False, "error": error}
        except Exception as e:
            print(f"Error en el reconocimiento facial: {str(e)}")
            raise
        
        # Convertir ambos DNIs a string para comparación
        dni_str = str(dni).strip()
        dni_reconocido_str = str(dni_reconocido).strip()
        
        print(f"Comparando DNIs:")
        print(f"DNI de sesión (tipo {type(dni)}): '{dni_str}'")
        print(f"DNI reconocido (tipo {type(dni_reconocido)}): '{dni_reconocido_str}'")
        
        if dni_str != dni_reconocido_str:
            print(f"El DNI reconocido ({dni_reconocido_str}) no coincide con el DNI de la sesión ({dni_str})")
            return {"success": False, "error": "El rostro no coincide con el DNI ingresado"}
        
        print(f"Reconocimiento exitoso para DNI: {dni_str}")
        return {
            "success": True,
            "nombre": dni_reconocido_str,
            "dni": dni_str
        }
    except Exception as e:
        print(f"Error en el procesamiento de la imagen: {str(e)}")
        return {"success": False, "error": str(e)}
