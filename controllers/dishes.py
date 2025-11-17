import json 
import logging
from datetime import datetime
from fastapi import HTTPException
from models.dishes import Dish
from models.dishes_ingredients import DishIngredient
from utlis.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_dish(dish: Dish) -> Dish:
    
    sqlscript: str = """
        insert into [kitchens].[dishes] ([restaurant_id], [name], [price], [type])
        values (?,?,?,?)
    """

    params = [
        dish.restaurant_id,
        dish.name,
        dish.price,
        dish.type
    ]
    
    insert_result = None
    
    try:
        insert_result = await execute_query_json(sqlscript, params=params,needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al crear el plato: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
        where name = ?
    """
    
    params = [dish.name]
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato creado: {str(e)}")
        
async def get_one_dish(id: int) -> Dish:
    
    selectscript: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
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
            raise HTTPException(status_code=404, detail=f"Plato no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato: {str(e)}")
    
async def get_all_dishes() -> list[Dish]:
    
    selectscript: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
    """
    
    result_dict = []
    
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener los platos: {str(e)}")
    
async def update_dish(dish: Dish) -> Dish:
    
    dict = dish.model_dump(exclude_unset=True)
    keys = [k for k in dict.keys()]
    keys.remove("id")
    variables = " = ?, ".join(keys) + " = ?"
    
    updatescript: str = f"""
        update [kitchens].[dishes]
        set {variables}
        where id = ?
    """
    params = [dict[k] for k in keys]
    params.append(dish.id)
    
    update_result = None
    
    try:
        update_result = await execute_query_json(updatescript, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al actualizar el plato: {str(e)}")
    
    sqlfind: str = """
        select [id]
            ,[restaurant_id]
            ,[name]
            ,[price]
            ,[type]
        from [kitchens].[dishes]
        where name = ?
    """
    
    params = [dish.name]
    
    result_dict = []
    
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)
        
        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el plato actualizado: {str(e)}")
    
async def delete_dish(id: int) -> str:
    
    deletescript: str = """
        delete from [kitchens].[dishes]
        where id = ?
    """
    
    params = [id]
    
    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "Plato eliminado correctamente"
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error al eliminar el plato: {str(e)}")
    
#================= Dish Ingredients Controllers =================#

async def add_ingredient_to_dish(dish_id: int, ingredient_id: int) -> DishIngredient:
    
    insert_script: str = """
        insert into [kitchens].[dishes_ingredients] ([dish_id],[ingredient_id],[availability_date],[active])
        values (?,?,?,?);
    """
    
    params = [
        dish_id, 
        ingredient_id,
        datetime.now(),
        True
        ]
    
    try:
        await execute_query_json(insert_script, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar el ingrediente al plato: {e}")
    
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
    
    params = [dish_id, ingredient_id]
    
    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el ingrediente del plato: {e}")
    
async def get_one_ingredient(dish_id: int, ingredient_id: int) -> DishIngredient:
    
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
    
    params = [dish_id, ingredient_id]
    
    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="Ingrediente no encontrado para el plato")
        return dict_result[0]
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener el ingrediente del plato: {e}")
    
async def get_all_ingredients(dish_id: int) -> list[DishIngredient]:
    
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
    
    params = [dish_id]
    
    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron ingredientes para el plato")
        return dict_result
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=f"Error al obtener los ingredientes del plato: {e}")
    
async def update_ingredient(ingredient_data: DishIngredient) -> DishIngredient:
    
    dict = ingredient_data.model_dump(exclude_none=True)
    keys = [k for k in dict.keys()]
    keys.remove("dish_id")
    keys.remove("ingredient_id")
    
    variables = " = ?, ".join(keys) + " = ?"
    
    updatescript: str = f"""
        update [kitchens].[dishes_ingredients]
        set {variables}
        where [dish_id]=? and [ingredient_id]=?;
    """
    
    params = [dict[v] for v in keys]
    params.append(ingredient_data.dish_id)
    params.append(ingredient_data.ingredient_id)
    
    try:
        await execute_query_json(updatescript, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el ingrediente del plato: {e}")
    
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
    
    params = [ingredient_data.dish_id, ingredient_data.ingredient_id]
    
    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el ingrediente del plato: {e}")
    
async def remove_ingredient(dish_id: int, ingredient_id: int) -> str:
    
    delete_script = """
        delete from kitchens.dishes_ingredients
        where [dish_id] = ? and [ingredient_id] = ?;
    """
    
    params = [dish_id, ingredient_id]
    
    try:
        await execute_query_json(delete_script, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el ingrediente del plato: {e}")