# Rutas relacionadas con los dishes
# Importar las librerías necesarias
# Importar FastAPI APIRouter y status
# Librerías para manejo de modelos y controladores
# Importar modelos y controladores
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

# Crear enrutador de FastAPI para dishes
router = APIRouter(prefix="/dishes")

# --------------------------- DISHES ROUTES --------------------------- #

# Definir ruta para crear un nuevo dish
@router.post("/", tags=["Dishes"], status_code=status.HTTP_201_CREATED)
# Definir función para crear un nuevo dish
async def create_new_dish(dish_data: Dish):
    # Llamar a la función del controlador para crear el dish
    result = await create_dish(dish_data)
    # Devolver el resultado de la creación del dish
    return result

# Definir ruta para obtener un dish por ID
@router.get("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para obtener un dish por ID
async def get_one_dish_route(id: int):
    # Llamar a la función del controlador para obtener el dish
    result: Dish = await get_one_dish(id)
    # Devolver el dish obtenido
    return result

# Definir ruta para obtener todos los dishes
@router.get("/", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para obtener todos los dishes
async def get_all_dishes_route():
    # Llamar a la función del controlador para obtener todos los dishes
    result = await get_all_dishes()
    # Devolver la lista de dishes obtenida
    return result

# Definir ruta para actualizar un dish existente
@router.put("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para actualizar un dish existente
async def update_existing_dish(id: int, dish_data: Dish):
    # Asignar el ID del dish a los datos del dish
    dish_data.id = id
    # Llamar a la función del controlador para actualizar el dish
    result = await update_dish(dish_data)
    # Devolver el resultado de la actualización del dish
    return result

# Definir ruta para eliminar un dish por ID
@router.delete("/{id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para eliminar un dish por ID
async def delete_dish_route(id: int):
    # Llamar a la función del controlador para eliminar el dish
    result = await delete_dish(id)
    # Devolver el resultado de la eliminación
    return result

# --------------------------- DISHES INGREDIENTS ROUTES --------------------------- #

# Definir ruta para agregar un ingrediente a un plato
@router.post("/{id}/ingredients", tags=["Dishes"], status_code=status.HTTP_201_CREATED)
# Definir función para agregar un ingrediente a un plato
async def add_ingredient_to_dish_route(id: int, ingredient_data: DishIngredient):
    # Llamar a la función del controlador para agregar el ingrediente al plato
    result = await add_ingredient_to_dish(id, ingredient_data.ingredient_id)
    # Devolver el resultado de la adición del ingrediente al plato
    return result 

# Definir ruta para obtener un ingrediente específico de un plato
@router.get("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para obtener un ingrediente específico de un plato
async def get_one_ingredient_route(id: int, ingredient_id: int):
    # Llamar a la función del controlador para obtener el ingrediente del plato
    result = await get_one_ingredient(id, ingredient_id)
    # Devolver el ingrediente obtenido
    return result

# Definir ruta para obtener todos los ingredientes de un plato
@router.get("/{id}/ingredients/", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para obtener todos los ingredientes de un plato
async def get_all_ingredients_route(id: int):
    # Llamar a la función del controlador para obtener todos los ingredientes del plato
    result = await get_all_ingredients(id)
    # Devolver la lista de ingredientes obtenida
    return result

# Definir ruta para actualizar un ingrediente de un plato
@router.put("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_200_OK)
# Definir función para actualizar un ingrediente de un plato
async def update_ingredient_route(id: int, ingredient_id: int, ingredient_data: DishIngredient):
    # Asignar los IDs del plato y del ingrediente a los datos del ingrediente
    ingredient_data.dish_id = id
    # Asignar el ID del ingrediente a los datos del ingrediente
    ingredient_data.ingredient_id = ingredient_id
    # Llamar a la función del controlador para actualizar el ingrediente del plato
    result = await update_ingredient(ingredient_data)
    # Devolver el resultado de la actualización del ingrediente del plato
    return result

# Definir ruta para eliminar un ingrediente de un plato
@router.delete("/{id}/ingredients/{ingredient_id}", tags=["Dishes"], status_code=status.HTTP_204_NO_CONTENT)
# Definir función para eliminar un ingrediente de un plato
async def remove_ingredient_route(id: int, ingredient_id: int):
    # Llamar a la función del controlador para eliminar el ingrediente del plato
    result = await remove_ingredient(id, ingredient_id)
    # Devolver el estado de la eliminación
    return result