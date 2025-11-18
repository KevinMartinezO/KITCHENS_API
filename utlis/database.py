# Módulo para la gestión de la conexión a la base de datos y ejecución de consultas SQL.
# Incluye funciones para conectarse a la base de datos, ejecutar consultas y devolver resultados en formato JSON.
# Importar librerías necesarias
# Librerías para manejo de entorno, base de datos, logging, JSON y asincronía
from dotenv import load_dotenv
import os
import pyodbc
import logging
import json
import asyncio

# Cargar  de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

# Configuración de la conexión a la base de datos desde variables de entorno
driver: str = os.getenv("SQL_DRIVER")
server: str = os.getenv("SQL_SERVER")
database: str = os.getenv("SQL_DATABASE")
username: str = os.getenv("SQL_USERNAME")
password: str = os.getenv("SQL_PASSWORD")

# Construir la cadena de conexión
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Función para obtener una conexión a la base de datos
async def get_db_connection():
    # Intentar conectar a la base de datos
    try:
        # Registrar intento de conexión
        logger.info("Conectando con la base de datos...")
        # Establecer conexión
        conn = pyodbc.connect(connection_string, timeout=5)
        # Registrar éxito de conexión
        logger.info("Conectado a la base de datos exitosamente.")
        # Devolver la conexión
        return conn
    # Manejo de errores de conexión
    except pyodbc.Error as e:
        # Registrar error de pyodbc
        logger.error(f"Error de pyodbc al conectar a la base de datos: {e}")
        # Relanzar excepción con mensaje personalizado
        raise Exception("No se pudo conectar a la base de datos") from e
    # Manejo de errores inesperados
    except Exception as e:
        # Registrar error inesperado
        logger.error(f"Error inesperado al conectar a la base de datos: {e}")
        # Relanzar la excepción
        raise

# Función para ejecutar una consulta SQL y devolver los resultados en formato JSON
async def execute_query_json(sql_template, params=None, needs_commit=False):

    # Inicializar variables
    conn = None
    cursor = None
    # Iniciar bloque try
    try:
        # Obtener conexión y cursor
        conn = await get_db_connection()
        # Obtener cursor
        cursor = conn.cursor()
        # Registrar la consulta que se va a ejecutar
        param_info = "(sin parámetros)" if not params else f"(con {len(params)} parámetros)"
        # Registrar la consulta SQL
        logger.info(f"Ejecutando consulta {param_info}: {sql_template}")
        
        # Ejecutar la consulta con o sin parámetros
        if params:
            # Ejecutar con parámetros
            cursor.execute(sql_template, params)
        # Ejecutar sin parámetros
        else:
            # Ejecutar sin parámetros
            cursor.execute(sql_template)
            
        # Procesar los resultados
        results = []
        # Verificar si la consulta devolvió columnas
        if cursor.description:
            # Obtener nombres de columnas
            columns = [column[0] for column in cursor.description]
            # Registrar las columnas obtenidas
            logger.info(f"Columnas obtenidas: {columns}")
            # Iterar sobre las filas devueltas
            for row in cursor.fetchall():
                # Procesar cada fila para convertir tipos de datos no serializables
                processed_row = [str(item) if isinstance(item, (bytes, bytearray)) else item for item in row]
                # Agregar fila procesada a resultados como diccionario
                results.append(dict(zip(columns, processed_row)))
        # Si no hay columnas devueltas
        else:
            # Registrar que no se devolvieron columnas
             logger.info("La consulta no devolvió columnas (posiblemente INSERT/UPDATE/DELETE).")

        # Realizar commit si es necesario
        if needs_commit:
            # Registrar commit
            logger.info("Realizando commit de la transacción.")
            # Realizar commit
            conn.commit()
        
        # Devolver resultados en formato JSON
        return json.dumps(results, default=str)

    # Manejo de errores de pyodbc
    except pyodbc.Error as e:
        # Registrar error de pyodbc
        logger.error(f"Error ejecutando la consulta (SQLSTATE: {e.args[0]}): {str(e)}")
        # Hacer rollback si es necesario
        if conn and needs_commit:
            # Intentar hacer rollback
            try:
                # Registrar intento de rollback
                logger.warning("Realizando rollback debido a error.")
                # Hacer rollback
                conn.rollback()
            # Manejo de errores durante el rollback    
            except pyodbc.Error as rb_e:
                # Registrar error durante el rollback
                 logger.error(f"Error durante el rollback: {rb_e}")

        # Relanzar excepción con mensaje personalizado
        raise Exception(f"Error ejecutando consulta: {str(e)}") from e
    # Manejo de errores inesperados
    except Exception as e:
        # Registrar error inesperado
        logger.error(f"Error inesperado durante la ejecución de la consulta: {str(e)}")
        # Relanzar la excepción
        raise
    # Asegurar el cierre de cursor y conexión
    finally:
        # Cerrar cursor y conexión si existen
        if cursor:
            # Cerrar cursor
            cursor.close()
        # Cerrar conexión
        if conn:
            # Cerrar conexión
            conn.close()
            # Registrar cierre de conexión
            logger.info("Conexión cerrada.")