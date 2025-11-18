# Rutas relacionadas con los restaurantes
# Importar las librerías necesarias
# Importar FastAPI APIRouter y status
# Librerías para manejo de modelos y controladores
# Importar modelos y controladores
from fastapi import APIRouter, status
from models.restaurants import Restaurant
from controllers.restaurants import(
    create_restaurant,
    update_restaurant,
    get_one_restaurant,
    get_all_restaurants,
    delete_restaurant
)

# Crear enrutador de FastAPI para restaurantes
router = APIRouter(prefix="/restaurants")

# --------------------------- RESTAURANTS ROUTES --------------------------- #

# Definir ruta para crear un nuevo restaurante
@router.post("/", tags=["Restaurants"], status_code=status.HTTP_201_CREATED)
# Definir función para crear un nuevo restaurante
async def create_new_restaurant(restaurant_data: Restaurant):
    # Llamar a la función del controlador para crear el restaurante
    result = await create_restaurant(restaurant_data)
    # Devolver el resultado de la creación del restaurante
    return result

# Definir ruta para obtener un restaurante por ID
@router.get("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
# Definir función para obtener un restaurante por ID
async def get_one_restaurant_route(id: int):
    # Llamar a la función del controlador para obtener el restaurante
    result: Restaurant = await get_one_restaurant(id)
    # Devolver el restaurante obtenido
    return result

# Definir ruta para obtener todos los restaurantes
@router.get("/", tags=["Restaurants"], status_code=status.HTTP_200_OK)
# Definir función para obtener todos los restaurantes
async def get_all_restaurants_route():
    # Llamar a la función del controlador para obtener todos los restaurantes
    result = await get_all_restaurants()
    # Devolver la lista de restaurantes obtenida 
    return result

# Definir ruta para actualizar un restaurante existente
@router.put("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
# Definir función para actualizar un restaurante existente
async def update_existing_restaurant(restaurant_data: Restaurant, id: int):
    # Asignar el ID del restaurante a los datos del restaurante
    restaurant_data.id = id
    # Llamar a la función del controlador para actualizar el restaurante
    result = await update_restaurant(restaurant_data)
    # Devolver el resultado de la actualización del restaurante
    return result

# Definir ruta para eliminar un restaurante por ID
@router.delete("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
# Definir función para eliminar un restaurante por ID
async def delete_restaurant_route(id: int):
    # Llamar a la función del controlador para eliminar el restaurante
    result = await delete_restaurant(id)
    # Devolver el resultado de la eliminación 
    return result