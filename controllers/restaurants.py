# Controlador para gestionar restaurantes en la base de datos
# Importar módulos necesarios
# Librerías para manejo de JSON, logging y excepciones HTTP
import json 
import logging
from fastapi import HTTPException
from models.restaurants import Restaurant
from utlis.database import execute_query_json

# Configurar logging
logging.basicConfig(level=logging.INFO)
# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

# ------------------------- Funciones CRUD para la entidad Restaurante -------------------------

# Crear un nuevo restaurante
async def create_restaurant(restaurant: Restaurant) -> Restaurant:
    
    # Script SQL para insertar un nuevo restaurante
    sqlscript: str = """
        insert into [kitchens].[restaurants] ([name], [address], [phone])
        values (?,?,?)
    """

    # Parámetros para la consulta SQL
    params = [
        restaurant.name,
        restaurant.address,
        restaurant.phone
    ]
    
    # Resultado de la inserción
    insert_result = None
    
    # Realizar la inserción en la base de datos
    try:
        # Ejecutar la consulta SQL para insertar el restaurante
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    # Manejo de errores durante la inserción
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al crear el restaurante: {str(e)}")
    
    # Obtener el restaurante recién creado para devolverlo
    sqlfind: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where address = ?
    """
    
    # Parámetros para buscar el restaurante recién creado
    params = [restaurant.address]
    
    # Resultado de la búsqueda
    try:
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver el primer restaurante encontrado
        if len(result_dict) > 0:
            # Devolver el primer restaurante encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante creado: {str(e)}")
        
# Obtener un restaurante por su ID
async def get_one_restaurant(id: int) -> Restaurant:
    
    # Script SQL para seleccionar un restaurante por su ID
    selectscript: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where id = ?
    """
    # Parámetros para la consulta SQL
    params = [id]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el restaurante por ID
        result = await execute_query_json(selectscript, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el restaurante encontrado o lanzar una excepción si no se encuentra
        if len(result_dict) > 0:
            # Devolver el primer restaurante encontrado
            return result_dict[0]
        # Si no se encuentra, lanzar una excepción HTTP 404
        else:
            # Lanzar una excepción HTTP 404 indicando que el restaurante no fue encontrado
            raise HTTPException(status_code=404, detail=f"Restaurante no encontrado")
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante: {str(e)}")
    
# Obtener todos los restaurantes
async def get_all_restaurants() -> list[Restaurant]:
    
    # Script SQL para seleccionar todos los restaurantes
    selectscript: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
    """
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener todos los restaurantes
        result = await execute_query_json(selectscript)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver la lista de restaurantes encontrados
        return result_dict
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener los restaurantes: {str(e)}")
    
# Actualizar un restaurante existente    
async def update_restaurant(restaurant: Restaurant) -> Restaurant:
    
    # Script SQL para actualizar un restaurante existente
    dict = restaurant.model_dump(exclude_unset=True)
    # Generar dinámicamente la parte de actualización del script SQL
    keys = [k for k in dict.keys()]
    # Excluir la clave "id" de la actualización
    keys.remove("id")
    # Crear la cadena de variables para la consulta SQL
    variables = " = ?, ".join(keys) + " = ?"
    
    # Script SQL de actualización
    updatescript: str = f"""
        update [kitchens].[restaurants]
        set {variables}
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [dict[k] for k in keys]
    # Agregar el ID del restaurante al final de los parámetros
    params.append(restaurant.id)
    
    # Resultado de la actualización
    update_result = None
    
    # Realizar la actualización en la base de datos
    try:
        # Ejecutar la consulta SQL para actualizar el restaurante
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    # Manejo de errores durante la actualización
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al actualizar el restaurante: {str(e)}")
    
    # Obtener el restaurante actualizado para devolverlo
    sqlfind: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where address = ?
    """
    
    # Parámetros para buscar el restaurante actualizado
    params = [restaurant.address]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el restaurante actualizado
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el primer restaurante encontrado
        if len(result_dict) > 0:
            # Devolver el primer restaurante encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante actualizado: {str(e)}")

# Eliminar un restaurante por su ID    
async def delete_restaurant(id: int) -> str:
    
    # Script SQL para eliminar un restaurante por su ID
    deletescript: str = """
        delete from [kitchens].[restaurants]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Realizar la eliminación en la base de datos
    try:
        # Ejecutar la consulta SQL para eliminar el restaurante
        await execute_query_json(deletescript, params=params, needs_commit=True)
        # Devolver un mensaje de éxito
        return "Restaurante eliminado correctamente"
    # Manejo de errores durante la eliminación
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al eliminar el restaurante: {str(e)}")