# Controlador para gestionar restaurantes en la base de datos
# Importar módulos necesarios
# Librerías para manejo de JSON, logging y excepciones HTTP
import json 
import logging
from fastapi import HTTPException
from models.providers import Provider
from utlis.database import execute_query_json

# Configurar logging
logging.basicConfig(level=logging.INFO)
# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

# ------------------------- Funciones CRUD para la entidad Proveedor -------------------------

# Crear un nuevo proveedor
async def create_provider(provider: Provider) -> Provider:
    
    # Script SQL para insertar un nuevo proveedor
    sqlscript: str = """
        insert into [kitchens].[providers] ([name], [phone], [address])
        values (?,?,?)
    """
    # Parámetros para la consulta SQL
    params = [
        provider.name,
        provider.phone,
        provider.address
    ]
    
    # Resultado de la inserción
    insert_result = None
    
    # Realizar la inserción en la base de datos
    try:
        # Ejecutar la consulta SQL para insertar el proveedor
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    # Manejo de errores durante la inserción
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al crear el proveedor: {str(e)}")
    
    # Obtener el proveedor recién creado para devolverlo
    sqlfind: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
        where address = ?
    """
    
    # Parámetros para buscar el proveedor recién creado
    params = [provider.address]
    
    # Resultado de la búsqueda
    try:
        # Realizar la búsqueda en la base de datos
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver el primer proveedor encontrado
        if len(result_dict) > 0:
            # Retornar el primer proveedor encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda    
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor creado: {str(e)}")
        
# Obtener un proveedor por su ID
async def get_one_provider(id: int) -> Provider:
    
    # Script SQL para obtener un proveedor por su ID
    selectscript: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el proveedor por ID
        result = await execute_query_json(selectscript, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Retornar el proveedor si se encuentra
        if len(result_dict) > 0:
            # Retornar el primer proveedor encontrado
            return result_dict[0]
        # Si no se encuentra, lanzar una excepción HTTP 404
        else:
            # Lanzar una excepción HTTP 404 indicando que el proveedor no fue encontrado
            raise HTTPException(status_code=404, detail=f"Proveedor no encontrado")
    # Manejo de errores durante la búsqueda    
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor: {str(e)}")
    
# Obtener todos los proveedores    
async def get_all_providers() -> list[Provider]:
    
    # Script SQL para obtener todos los proveedores
    selectscript: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
    """
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener todos los proveedores
        result = await execute_query_json(selectscript)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver la lista de proveedores
        return result_dict
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener los proveedores: {str(e)}")
    
# Actualizar un proveedor existente    
async def update_provider(provider: Provider) -> Provider:
    
    # Script SQL para actualizar un proveedor
    dict = provider.model_dump(exclude_unset=True)
    # Generar dinámicamente la parte de actualización del script SQL
    keys = [k for k in dict.keys()]
    # Quitar la clave 'id' de las claves a actualizar
    keys.remove("id")
    # Generar la cadena de variables para el SET del SQL
    variables = " = ?, ".join(keys) + " = ?"
    
    # Script SQL para la actualización
    updatescript: str = f"""
        update [kitchens].[providers]
        set {variables}
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [dict[k] for k in keys]
    # Agregar el ID del proveedor al final de los parámetros
    params.append(provider.id)
    
    # Resultado de la actualización
    update_result = None
    
    # Realizar la actualización en la base de datos
    try:
        # Ejecutar la consulta SQL para actualizar el proveedor
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    # Manejo de errores durante la actualización
    except Exception as e:
        # Registrar el error    
        raise HTTPException(status_code=404, detail=f"Error al actualizar el proveedor: {str(e)}")
    
    # Obtener el proveedor actualizado para devolverlo
    sqlfind: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
        where address = ?
    """
    
    # Parámetros para buscar el proveedor actualizado
    params = [provider.address]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el proveedor actualizado
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el primer proveedor encontrado
        if len(result_dict) > 0:
            # Devolver el primer proveedor encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda    
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor actualizado: {str(e)}")
   
# Eliminar un proveedor por su ID    
async def delete_provider(id: int) -> str:
    
    # Script SQL para eliminar un proveedor por su ID
    deletescript: str = """
        delete from [kitchens].[providers]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Realizar la eliminación en la base de datos
    try:
        # Ejecutar la consulta SQL para eliminar el proveedor
        await execute_query_json(deletescript, params=params, needs_commit=True)
        # Devolver un mensaje de éxito
        return "Proveedor eliminado correctamente"
    # Manejo de errores durante la eliminación
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al eliminar el proveedor: {str(e)}")