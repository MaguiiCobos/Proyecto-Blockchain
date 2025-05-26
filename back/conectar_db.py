import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # Dejá vacío si no usás contraseña en XAMPP
        database="blockchain"  # nombre de la BD de MySQL
    )

    if conexion.is_connected():
        print(" Conexión exitosa a la base de datos MySQL")

except mysql.connector.Error as e:
    print(" Error al conectar a MySQL:", e)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print(" Conexión cerrada")
