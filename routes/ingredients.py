from fastapi import APIRouter, status
from models.ingredients import Ingredient
from controllers.ingredients import(
    create_ingredient,
    update_ingredient,
    get_one_ingredient,
    get_all_ingredients,
    delete_ingredient
)

router = APIRouter(prefix="/ingredients")

@router.post("/", tags=["Ingredients"], status_code=status.HTTP_201_CREATED)
async def create_new_ingredient(ingredient_data: Ingredient):
    result = await create_ingredient(ingredient_data)
    return result

@router.put("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
async def update_existing_ingredient(ingredient_data: Ingredient, id: int):
    ingredient_data.id = id
    result = await update_ingredient(ingredient_data)
    return result

@router.get("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
async def get_one_ingredient_route(id: int):
    result: Ingredient = await get_one_ingredient(id)
    return result

@router.get("/", tags=["Ingredients"], status_code=status.HTTP_200_OK)
async def get_all_ingredients_route():
    result = await get_all_ingredients()
    return result

@router.delete("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
async def delete_ingredient_route(id: int):
    result = await delete_ingredient(id)
    return result