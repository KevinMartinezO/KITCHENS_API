# Rutas relacionadas con los ingredients
# Importar las librerías necesarias
# Importar FastAPI APIRouter y status
# Librerías para manejo de modelos y controladores
# Importar modelos y controladores
from fastapi import APIRouter, status
from models.ingredients import Ingredient
from controllers.ingredients import(
    create_ingredient,
    update_ingredient,
    get_one_ingredient,
    get_all_ingredients,
    delete_ingredient
)

# Crear enrutador de FastAPI para ingredients
router = APIRouter(prefix="/ingredients")

# --------------------------- INGREDIENTS ROUTES --------------------------- #

# Definir ruta para crear un nuevo ingredient
@router.post("/", tags=["Ingredients"], status_code=status.HTTP_201_CREATED)
# Definir función para crear un nuevo ingredient
async def create_new_ingredient(ingredient_data: Ingredient):
    # Llamar a la función del controlador para crear el ingredient
    result = await create_ingredient(ingredient_data)
    # Devolver el resultado de la creación del ingredient
    return result

# Definir ruta para actualizar un ingredient existente
@router.put("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
# Definir función para actualizar un ingredient existente
async def update_existing_ingredient(ingredient_data: Ingredient, id: int):
    # Asignar el ID del ingredient a los datos del ingredient
    ingredient_data.id = id
    # Llamar a la función del controlador para actualizar el ingredient
    result = await update_ingredient(ingredient_data)
    # Devolver el resultado de la actualización del ingredient
    return result

# Definir ruta para obtener un ingredient por ID
@router.get("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
# Definir función para obtener un ingredient por ID
async def get_one_ingredient_route(id: int):
    # Llamar a la función del controlador para obtener el ingredient
    result: Ingredient = await get_one_ingredient(id)
    # Devolver el ingredient obtenido
    return result

# Definir ruta para obtener todos los ingredients
@router.get("/", tags=["Ingredients"], status_code=status.HTTP_200_OK)
# Definir función para obtener todos los ingredients
async def get_all_ingredients_route():
    # Llamar a la función del controlador para obtener todos los ingredients
    result = await get_all_ingredients()
    # Devolver la lista de ingredients obtenida
    return result

# Definir ruta para eliminar un ingredient por ID
@router.delete("/{id}", tags=["Ingredients"], status_code=status.HTTP_200_OK)
# Definir función para eliminar un ingredient por ID
async def delete_ingredient_route(id: int):
    # Llamar a la función del controlador para eliminar el ingredient
    result = await delete_ingredient(id)
    # Devolver el resultado de la eliminación
    return result