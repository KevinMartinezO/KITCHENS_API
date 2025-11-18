# Controlador para gestionar ingredientes en la base de datos
# Importar módulos necesarios
# Librerías para manejo de JSON, logging y excepciones HTTP
import json 
import logging
from fastapi import HTTPException
from models.ingredients import Ingredient
from utlis.database import execute_query_json

# Configurar logging
logging.basicConfig(level=logging.INFO)
# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

# ------------------------- Funciones CRUD para la entidad Ingrediente -------------------------

# Crear un nuevo ingrediente
async def create_ingredient(ingredient: Ingredient) -> Ingredient:
    
    # Script SQL para insertar un nuevo ingrediente
    sqlscript: str = """
        insert into [kitchens].[ingredients] ([provider_id], [name], [category])
        values (?,?,?)
    """
    # Parámetros para la consulta SQL
    params = [
        ingredient.provider_id,
        ingredient.name,
        ingredient.category
    ]
    
    # Resultado de la inserción
    insert_result = None
    
    # Realizar la inserción en la base de datos
    try:
        # Ejecutar la consulta SQL para insertar el ingrediente
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    # Manejo de errores durante la inserción
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al crear el ingrediente: {str(e)}")
    
    # Obtener el ingrediente recién creado para devolverlo
    sqlfind: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
        where name = ?
    """
    
    # Parámetros para buscar el ingrediente recién creado
    params = [ingredient.name]
    
    # Resultado de la búsqueda
    try:
        # Realizar la búsqueda en la base de datos
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver el primer ingrediente encontrado
        if len(result_dict) > 0:
            # Devolver el primer ingrediente encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente creado: {str(e)}")
        
# Obtener un ingrediente por su ID
async def get_one_ingredient(id: int) -> Ingredient:
    
    # Script SQL para obtener un ingrediente por su ID
    selectscript: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Resultado de la consulta
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el ingrediente por ID
        result = await execute_query_json(selectscript, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el ingrediente si se encuentra
        if len(result_dict) > 0:
            # Devolver el primer ingrediente encontrado
            return result_dict[0]
        # Si no se encuentra, lanzar una excepción HTTP 404
        else:
            # Lanzar una excepción HTTP 404 indicando que el ingrediente no fue encontrado
            raise HTTPException(status_code=404, detail=f"Ingrediente no encontrado")
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente: {str(e)}")
    
# Obtener todos los ingredientes
async def get_all_ingredients() -> list[Ingredient]:
    
    # Script SQL para obtener todos los ingredientes
    selectscript: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
    """
    
    # Resultado de la consulta
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener todos los ingredientes
        result = await execute_query_json(selectscript)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver la lista de ingredientes
        return result_dict
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener los ingredientes: {str(e)}")
    
# Actualizar un ingrediente existente    
async def update_ingredient(ingredient: Ingredient) -> Ingredient:
    
    # Script SQL para actualizar un ingrediente existente
    dict = ingredient.model_dump(exclude_unset=True)
    # Generar la parte de la consulta SQL para los campos a actualizar
    keys = [k for k in dict.keys()]
    # Excluir la clave "id" de los campos a actualizar
    keys.remove("id")
    # Generar dinámicamente las variables para la consulta SQL
    variables = " = ?, ".join(keys) + " = ?"
    
    # Script SQL para la actualización
    updatescript: str = f"""
        update [kitchens].[ingredients]
        set {variables}
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [dict[k] for k in keys]
    # Agregar el ID del ingrediente al final de los parámetros
    params.append(ingredient.id)
    
    # Resultado de la actualización
    update_result = None
    
    # Realizar la actualización en la base de datos
    try:
        # Ejecutar la consulta SQL para actualizar el ingrediente
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    # Manejo de errores durante la actualización
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al actualizar el ingrediente: {str(e)}")
    
    # Obtener el ingrediente actualizado para devolverlo
    sqlfind: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
        where name = ?
    """
    
    # Parámetros para buscar el ingrediente actualizado
    params = [ingredient.name]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el ingrediente actualizado
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el ingrediente actualizado si se encuentra
        if len(result_dict) > 0:
            # Devolver el primer ingrediente encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente actualizado: {str(e)}")
    
# Eliminar un ingrediente por su ID
async def delete_ingredient(id: int) -> str:
    
    # Script SQL para eliminar un ingrediente por su ID
    deletescript: str = """
        delete from [kitchens].[ingredients]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Realizar la eliminación en la base de datos
    try:
        # Ejecutar la consulta SQL para eliminar el ingrediente
        await execute_query_json(deletescript, params=params, needs_commit=True)
        # Devolver un mensaje de éxito
        return "Ingrediente eliminado correctamente"
    # Manejo de errores durante la eliminación
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al eliminar el ingrediente: {str(e)}")