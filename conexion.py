# Importamos psycopg para conectarnos a PostgreSQL
import psycopg

# Importamos load_dotenv para leer el archivo .env
from dotenv import load_dotenv

# Importamos os para acceder a las variables de entorno
import os

# Cargamos las variables del archivo .env
load_dotenv()


# Funcion para establecer la conexion
def conectar():

    try:

        # Establecemos la conexion con PostgreSQL
        conexion = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        # Retornamos la conexion
        return conexion

    except psycopg.Error as error:

        # Mostramos el error de conexion
        print("Error al conectar con PostgreSQL:", error)

        return None
