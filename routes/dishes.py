from fastapi import APIRouter, status
from models.dishes import Dish
from models.dishes_ingredients import DishIngredient
from controllers.dishes import(
    create_dish,
    update_dish,
    get_one_dish,
    get_all_dishes,
    delete_dish,
    add_ingredient_to_dish,
    update_ingredient,
    get_one_ingredient,
    get_all_ingredients,
    remove_ingredient
)

router = APIRouter(prefix="/dishes")

@router.post("/", tags=["Dishes"], status_code=status.HTTP_201_CREATED)
async def create_new_dish(dish_data: Dish):
    result = await create_dish(dish_data)
    return result

@router.get("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def get_one_dish_route(id: int):
    result: Dish = await get_one_dish(id)
    return result

@router.get("/", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def get_all_dishes_route():
    result = await get_all_dishes()
    return result

@router.put("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def update_existing_dish(dish_data: Dish, id: int):
    dish_data.id = id
    result = await update_dish(dish_data)
    return result

@router.delete("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def delete_dish_route(id: int):
    result = await delete_dish(id)
    return result

# --- INGREDIENTS IN DISHES ROUTES --- #

@router.post("/{id}/ingredients", tags=["Dishes"], status_code=status.HTTP_201_CREATED)
async def add_ingredient_to_dish_route(id: int, ingredient_data: DishIngredient):
    result = await add_ingredient_to_dish(id, ingredient_data.ingredient_id)
    return result 

@router.get("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def get_one_ingredient_route(id: int, ingredient_id: int):
    result = await get_one_ingredient(id, ingredient_id)
    return result

@router.get("/{id}/ingredients/", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def get_all_ingredients_route(id: int):
    result = await get_all_ingredients(id)
    return result

@router.put("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
async def update_ingredient_route(id: int, ingredient_id: int, ingredient_data: DishIngredient):
    ingredient_data.dish_id = id
    ingredient_data.ingredient_id = ingredient_id
    result = await update_ingredient(ingredient_data)
    return result

@router.delete("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_ingredient_route(id: int, ingredient_id: int):
    status: str = await remove_ingredient(id, ingredient_id)
    return status

