# Controlador para gestionar platos en la base de datos
# Importar módulos necesarios
# Librerías para manejo de JSON, logging, fechas y excepciones HTTP
import json 
import logging
from datetime import datetime
from fastapi import HTTPException
from models.dishes import Dish
from models.dishes_ingredients import DishIngredient
from utlis.database import execute_query_json

# Configurar logging
logging.basicConfig(level=logging.INFO)
# Configurar el logger para este módulo
logger = logging.getLogger(__name__)

# ------------------------- Funciones CRUD para la entidad Plato -------------------------

# Crear un nuevo plato
async def create_dish(dish: Dish) -> Dish:
    
    # Script SQL para insertar un nuevo plato
    sqlscript: str = """
        insert into [kitchens].[dishes] ([restaurant_id], [name], [price], [type])
        values (?,?,?,?)
    """
    
    # Parámetros para la consulta SQL
    params = [
        dish.restaurant_id,
        dish.name,
        dish.price,
        dish.type
    ]
    
    # Resultado de la inserción
    insert_result = None
    
    # Realizar la inserción en la base de datos
    try:
        # Ejecutar la consulta SQL para insertar el plato
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    # Manejo de errores durante la inserción
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al crear el plato: {str(e)}")
    
    # Obtener el plato recién creado para devolverlo
    sqlfind: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
        where name = ?
    """
    
    # Parámetros para buscar el plato recién creado
    params = [dish.name]
    
    # Resultado de la búsqueda
    try:
        # Realizar la búsqueda en la base de datos
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver el primer plato encontrado
        if len(result_dict) > 0:
            # Devolver el primer plato encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda    
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato creado: {str(e)}")
        
# Obtener un plato por su ID        
async def get_one_dish(id: int) -> Dish:
    
    # Script SQL para obtener un plato por su ID
    selectscript: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Resultado de la consulta
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el plato por ID
        result = await execute_query_json(selectscript, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Retornar el plato si se encuentra
        if len(result_dict) > 0:
            # Retornar el primer plato encontrado
            return result_dict[0]
        # Si no se encuentra, lanzar una excepción HTTP 404
        else:
            # Lanzar una excepción HTTP 404 indicando que el plato no fue encontrado
            raise HTTPException(status_code=404, detail=f"Plato no encontrado")
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato: {str(e)}")
    
# Obtener todos los platos
async def get_all_dishes() -> list[Dish]:
    
    # Script SQL para obtener todos los platos
    selectscript: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
    """
    
    # Resultado de la consulta
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener todos los platos
        result = await execute_query_json(selectscript)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        # Devolver la lista de platos
        return result_dict
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener los platos: {str(e)}")
    
# Actualizar un plato existente    
async def update_dish(dish: Dish) -> Dish:
    
    # Preparar los datos para la actualización
    dict = dish.model_dump(exclude_unset=True)
    # Obtener las claves de los campos a actualizar
    keys = [k for k in dict.keys()]
    # Quitar la clave 'id' de las claves a actualizar
    keys.remove("id")
    # Generar la parte de la consulta SQL para los campos a actualizar
    variables = " = ?, ".join(keys) + " = ?"
    
    # Script SQL para la actualización
    updatescript: str = f"""
        update [kitchens].[dishes]
        set {variables}
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [dict[k] for k in keys]
    # Agregar el ID del plato al final de los parámetros
    params.append(dish.id)
    
    # Resultado de la actualización
    update_result = None
    
    # Realizar la actualización en la base de datos
    try:
        # Ejecutar la consulta SQL para actualizar el plato
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    # Manejo de errores durante la actualización
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al actualizar el plato: {str(e)}")
    
    # Obtener el plato actualizado para devolverlo
    sqlfind: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
        where name = ?
    """
    
    # Parámetros para buscar el plato actualizado
    params = [dish.name]
    
    # Resultado de la búsqueda
    result_dict = []
    
    # Realizar la búsqueda en la base de datos
    try:
        # Ejecutar la consulta SQL para obtener el plato actualizado
        result = await execute_query_json(sqlfind, params=params)
        # Convertir el resultado JSON a diccionario
        result_dict = json.loads(result)
        
        # Devolver el plato actualizado si se encuentra
        if len(result_dict) > 0:
            # Devolver el primer plato encontrado
            return result_dict[0]
        # Si no se encuentra, devolver una lista vacía
        else:
            # Devolver una lista vacía
            return []
    # Manejo de errores durante la búsqueda
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato actualizado: {str(e)}")
    
# Eliminar un plato por su ID    
async def delete_dish(id: int) -> str:
    
    # Script SQL para eliminar un plato por su ID
    deletescript: str = """
        delete from [kitchens].[dishes]
        where id = ?
    """
    
    # Parámetros para la consulta SQL
    params = [id]
    
    # Realizar la eliminación en la base de datos
    try:
        # Ejecutar la consulta SQL para eliminar el plato
        await execute_query_json(deletescript, params=params, needs_commit=True)
        # Devolver un mensaje de éxito
        return "Plato eliminado correctamente"
    # Manejo de errores durante la eliminación
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al eliminar el plato: {str(e)}")
    
# ------------------------- Funciones CRUD para la entidad Plato-Ingrediente -------------------------

# Agregar un ingrediente a un plato    
async def add_ingredient_to_dish(dish_id: int, ingredient_id: int) -> DishIngredient:
    
    # Script SQL para agregar un ingrediente a un plato
    insert_script: str = """
        insert into [kitchens].[dishes_ingredients] ([dish_id],[ingredient_id],[availability_date],[active])
        values (?,?,?,?);
    """
    
    # Parámetros para la consulta SQL
    params = [
        dish_id, 
        ingredient_id,
        datetime.now(),
        True
        ]
    
    # Realizar la inserción en la base de datos
    try:
        # Ejecutar la consulta SQL para agregar el ingrediente al plato
        await execute_query_json(insert_script, params=params, needs_commit=True)
    # Manejo de errores durante la inserción    
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=500, detail=f"Error al agregar el ingrediente al plato: {e}")
    
    # Obtener el ingrediente agregado para devolverlo
    select_script: str = """
        select
            di.ingredient_id,
            i.name as ingredient_name,
            i.provider_id,
            p.name as provider_name,
            d.restaurant_id,
            r.name as restaurant_name,
            di.availability_date,
            di.active
        from kitchens.dishes_ingredients di
        inner join kitchens.ingredients i
        on di.ingredient_id = i.id
        inner join kitchens.providers p
        on i.provider_id = p.id
        inner join kitchens.dishes d
        on di.dish_id = d.id
        inner join kitchens.restaurants r
        on d.restaurant_id = r.id
        where di.dish_id = ?
        and di.ingredient_id = ?;
    """
    # Parámetros para la consulta SQL
    params = [dish_id, ingredient_id]
    
    # Obtener y devolver el ingrediente agregado
    try:
        # Ejecutar la consulta SQL para obtener el ingrediente agregado
        result = await execute_query_json(select_script, params=params)
        # Convertir el resultado JSON a un diccionario y devolver el primer elemento
        return json.loads(result)[0]
    # Manejo de errores durante la obtención
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=500, detail=f"Error al obtener el ingrediente del plato: {e}")
    
# Obtener un ingrediente de un plato por sus IDs
async def get_one_ingredient(dish_id: int, ingredient_id: int) -> DishIngredient:
    
    # Script SQL para obtener un ingrediente de un plato por sus IDs
    select_script: str = """
        select
            di.ingredient_id,
            i.name as ingredient_name,
            i.provider_id,
            p.name as provider_name,
            d.restaurant_id,
            r.name as restaurant_name,
            di.availability_date,
            di.active
        from kitchens.dishes_ingredients di
        inner join kitchens.ingredients i
        on di.ingredient_id = i.id
        inner join kitchens.providers p
        on i.provider_id = p.id
        inner join kitchens.dishes d
        on di.dish_id = d.id
        inner join kitchens.restaurants r
        on d.restaurant_id = r.id
        where di.dish_id = ?
        and di.ingredient_id = ?;
    """
    
    # Parámetros para la consulta SQL
    params = [dish_id, ingredient_id]
    
    # Obtener y devolver el ingrediente del plato
    try:
        # Ejecutar la consulta SQL para obtener el ingrediente del plato
        result = await execute_query_json(select_script, params=params)
        # Convertir el resultado JSON a un diccionario
        dict_result = json.loads(result)
        # Verificar si el resultado está vacío
        if len(dict_result) == 0:
            # Lanzar una excepción HTTP 404 si no se encuentra el ingrediente
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado para el plato")
        # Devolver el primer ingrediente encontrado
        return dict_result[0]
    # Manejo de errores durante la obtención
    except HTTPException as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente del plato: {e}")

# Obtener todos los ingredientes de un plato
async def get_all_ingredients(dish_id: int) -> list[DishIngredient]:
    
    # Script SQL para obtener todos los ingredientes de un plato
    select_script: str = """
        select
            di.ingredient_id,
            i.name as ingredient_name,
            i.provider_id,
            p.name as provider_name,
            d.restaurant_id,
            r.name as restaurant_name,
            di.availability_date,
            di.active
        from kitchens.dishes_ingredients di
        inner join kitchens.ingredients i
        on di.ingredient_id = i.id
        inner join kitchens.providers p
        on i.provider_id = p.id
        inner join kitchens.dishes d
        on di.dish_id = d.id
        inner join kitchens.restaurants r
        on d.restaurant_id = r.id
        where di.dish_id = ?;
    """
    
    # Parámetros para la consulta SQL
    params = [dish_id]
    
    # Obtener y devolver los ingredientes del plato
    try:
        # Ejecutar la consulta SQL para obtener los ingredientes del plato
        result = await execute_query_json(select_script, params=params)
        # Convertir el resultado JSON a un diccionario
        dict_result = json.loads(result)
        # Verificar si el resultado está vacío
        if len(dict_result) == 0:
            # Lanzar una excepción HTTP 404 si no se encuentran ingredientes
            raise HTTPException(status_code=404, detail="No se encontraron ingredientes para el plato")
        # Devolver la lista de ingredientes encontrados
        return dict_result
    # Manejo de errores durante la obtención
    except HTTPException as e:
        # Registrar el error
        raise HTTPException(status_code=404, detail=f"Error al obtener los ingredientes del plato: {e}")
    
# Actualizar un ingrediente de un plato
async def update_ingredient(ingredient_data: DishIngredient) -> DishIngredient:
    
    # Preparar los datos para la actualización
    dict = ingredient_data.model_dump(exclude_none=True)
    # Obtener las claves de los campos a actualizar
    keys = [k for k in dict.keys()]
    # Eliminar las claves que no deben actualizarse
    keys.remove("dish_id")
    # Eliminar la clave ingredient_id que no debe actualizarse
    keys.remove("ingredient_id")
    
    # Generar la parte de la consulta SQL para los campos a actualizar
    variables = " = ?, ".join(keys) + " = ?"
    
    # Script SQL para la actualización
    updatescript: str = f"""
        update [kitchens].[dishes_ingredients]
        set {variables}
        where [dish_id]=? and [ingredient_id]=?;
    """
    
    # Parámetros para la consulta SQL
    params = [dict[v] for v in keys]
    # Agregar los IDs al final de los parámetros
    params.append(ingredient_data.dish_id)
    # Agregar el ID del ingrediente al final de los parámetros
    params.append(ingredient_data.ingredient_id)
    
    # Realizar la actualización en la base de datos
    try:
        # Ejecutar la consulta SQL para actualizar el ingrediente del plato
        await execute_query_json(updatescript, params=params, needs_commit=True)
    # Manejo de errores durante la actualización
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=500, detail=f"Error al actualizar el ingrediente del plato: {e}")
    
    # Obtener el ingrediente actualizado para devolverlo
    select_script: str = """
        select
            di.ingredient_id,
            i.name as ingredient_name,
            i.provider_id,
            p.name as provider_name,
            d.restaurant_id,
            r.name as restaurant_name,
            di.availability_date,
            di.active
        from kitchens.dishes_ingredients di
        inner join kitchens.ingredients i
        on di.ingredient_id = i.id
        inner join kitchens.providers p
        on i.provider_id = p.id
        inner join kitchens.dishes d
        on di.dish_id = d.id
        inner join kitchens.restaurants r
        on d.restaurant_id = r.id
        where di.dish_id = ?
        and di.ingredient_id = ?;
    """
    
    # Parámetros para la consulta SQL
    params = [ingredient_data.dish_id, ingredient_data.ingredient_id]
    
    # Obtener y devolver el ingrediente actualizado
    try:
        # Ejecutar la consulta SQL para obtener el ingrediente actualizado
        result = await execute_query_json(select_script, params=params)
        # Convertir el resultado JSON a un diccionario y devolver el primer elemento
        return json.loads(result)[0]
    # Manejo de errores durante la obtención
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=500, detail=f"Error al obtener el ingrediente del plato: {e}")
    
# Eliminar un ingrediente de un plato
async def remove_ingredient(dish_id: int, ingredient_id: int) -> str:
    
    # Script SQL para eliminar un ingrediente de un plato
    delete_script = """
        delete from kitchens.dishes_ingredients
        where [dish_id] = ? and [ingredient_id] = ?;
    """
    
    # Parámetros para la consulta SQL
    params = [dish_id, ingredient_id]
    
    # Realizar la eliminación en la base de datos
    try:
        # Ejecutar la consulta SQL para eliminar el ingrediente del plato
        await execute_query_json(delete_script, params=params, needs_commit=True)
        # Devolver un mensaje de éxito
        return "DELETED"
    # Manejo de errores durante la eliminación
    except Exception as e:
        # Registrar el error
        raise HTTPException(status_code=500, detail=f"Error al eliminar el ingrediente del plato: {e}")