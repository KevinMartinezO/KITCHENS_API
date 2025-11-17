import json 
import logging
from fastapi import HTTPException
from models.ingredients import Ingredient
from utlis.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_ingredient(ingredient: Ingredient) -> Ingredient:
    
    sqlscript: str = """
        insert into [kitchens].[ingredients] ([provider_id], [name], [category])
        values (?,?,?)
    """

    params = [
        ingredient.provider_id,
        ingredient.name,
        ingredient.category
    ]
    
    insert_result = None
    
    try:
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al crear el ingrediente: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
        where name = ?
    """
    
    params = [ingredient.name]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente creado: {str(e)}")
        
async def get_one_ingredient(id: int) -> Ingredient:
    
    selectscript: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
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
            raise HTTPException(status_code=404, detail=f"Ingrediente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente: {str(e)}")
    
async def get_all_ingredients() -> list[Ingredient]:
    
    selectscript: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
    """
    
    result_dict = []
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener los ingredientes: {str(e)}")
    
async def update_ingredient(ingredient: Ingredient) -> Ingredient:
    
    dict = ingredient.model_dump(exclude_unset=True)
    keys = [k for k in dict.keys()]
    keys.remove("id")
    variables = " = ?, ".join(keys) + " = ?"
    
    updatescript: str = f"""
        update [kitchens].[ingredients]
        set {variables}
        where id = ?
    """
    params = [dict[k] for k in keys]
    params.append(ingredient.id)
    
    update_result = None
    
    try:
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al actualizar el ingrediente: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[provider_id]
            ,[name]
            ,[category]
        from [kitchens].[ingredients]
        where name = ?
    """
    
    params = [ingredient.name]
    
    result_dict = []
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente actualizado: {str(e)}")
    
async def delete_ingredient(id: int) -> str:
    
    deletescript: str = """
        delete from [kitchens].[ingredients]
        where id = ?
    """
    
    params = [id]
    
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "Ingrediente eliminado correctamente"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al eliminar el ingrediente: {str(e)}")