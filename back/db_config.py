import os
from dotenv import load_dotenv

# Intentar cargar variables de entorno
try:
    load_dotenv()
except:
    pass

# Configuración por defecto de la base de datos
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'blockchain'),
    'port': 3306  # Puerto fijo para MySQL/MariaDB
}

# Imprimir la configuración (sin la contraseña)
print("Configuración de la base de datos:")
print(f"Host: {db_config['host']}")
print(f"Usuario: {db_config['user']}")
print(f"Base de datos: {db_config['database']}")
print(f"Puerto: {db_config['port']}")
