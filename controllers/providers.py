import json 
import logging
from fastapi import HTTPException
from models.providers import Provider
from utlis.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_provider(provider: Provider) -> Provider:
    
    sqlscript: str = """
        insert into [kitchens].[providers] ([name], [phone], [address])
        values (?,?,?)
    """

    params = [
        provider.name,
        provider.phone,
        provider.address
    ]
    
    insert_result = None
    
    try:
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al crear el proveedor: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
        where address = ?
    """
    params = [provider.address]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor creado: {str(e)}")
        
async def get_one_provider(id: int) -> Provider:
    
    selectscript: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
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
            raise HTTPException(status_code=404, detail=f"Proveedor no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor: {str(e)}")
    
async def get_all_providers() -> list[Provider]:
    
    selectscript: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
    """
    
    result_dict = []
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener los proveedores: {str(e)}")
    
async def update_provider(provider: Provider) -> Provider:
    
    dict = provider.model_dump(exclude_unset=True)
    keys = [k for k in dict.keys()]
    keys.remove("id")
    variables = " = ?, ".join(keys) + " = ?"
    
    updatescript: str = f"""
        update [kitchens].[providers]
        set {variables}
        where id = ?
    """
    
    params = [dict[k] for k in keys]
    params.append(provider.id)
    
    update_result = None
    
    try:
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al actualizar el proveedor: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[name]
            ,[phone]
            ,[address]
        from [kitchens].[providers]
        where address = ?
    """
    params = [provider.address]
    
    result_dict = []
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el proveedor actualizado: {str(e)}")
    
async def delete_provider(id: int) -> str:
    
    deletescript: str = """
        delete from [kitchens].[providers]
        where id = ?
    """
    
    params = [id]
    
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "Proveedor eliminado correctamente"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al eliminar el proveedor: {str(e)}")