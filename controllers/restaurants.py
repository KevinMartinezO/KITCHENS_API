import json 
import logging
from fastapi import HTTPException
from models.restaurants import Restaurant
from utlis.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_restaurant(restaurant: Restaurant) -> Restaurant:
    
    sqlscript: str = """
        insert into [kitchens].[restaurants] ([name], [address], [phone])
        values (?,?,?)
    """

    params = [
        restaurant.name,
        restaurant.address,
        restaurant.phone
    ]
    
    insert_result = None
    
    try:
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al crear el restaurante: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where address = ?
    """
    params = [restaurant.address]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante creado: {str(e)}")
        
async def get_one_restaurant(id: int) -> Restaurant:
    
    selectscript: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where id = ?
    """
    
    params = [id]
    
    result_dict = []
    
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)
        
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"Restaurante no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante: {str(e)}")
    
async def get_all_restaurants() -> list[Restaurant]:
    
    selectscript: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
    """
    
    result_dict = []
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener los restaurantes: {str(e)}")
    
async def update_restaurant(restaurant: Restaurant) -> Restaurant:
    
    dict = restaurant.model_dump(exclude_unset=True)
    keys = [k for k in dict.keys()]
    keys.remove("id")
    variables = " = ?, ".join(keys) + " = ?"
    
    updatescript: str = f"""
        update [kitchens].[restaurants]
        set {variables}
        where id = ?
    """
    
    params = [dict[k] for k in keys]
    params.append(restaurant.id)
    
    update_result = None
    
    try:
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al actualizar el restaurante: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[name]
            ,[address]
            ,[phone]
        from [kitchens].[restaurants]
        where address = ?
    """
    params = [restaurant.address]
    
    result_dict = []
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el restaurante actualizado: {str(e)}")
    
async def delete_restaurant(id: int) -> str:
    
    deletescript: str = """
        delete from [kitchens].[restaurants]
        where id = ?
    """
    
    params = [id]
    
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "Restaurante eliminado correctamente"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al eliminar el restaurante: {str(e)}")