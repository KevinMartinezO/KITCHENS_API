# Rutas relacionadas con los providers
# Importar las librerías necesarias
# Importar FastAPI APIRouter y status
# Librerías para manejo de modelos y controladores
# Importar modelos y controladores
from fastapi import APIRouter, status
from models.providers import Provider
from controllers.providers import(
    create_provider,
    update_provider,
    get_one_provider,
    get_all_providers,
    delete_provider
)

# Crear enrutador de FastAPI para providers
router = APIRouter(prefix="/providers")

# --------------------------- PROVIDERS ROUTES --------------------------- #

# Definir ruta para crear un nuevo provider
@router.post("/", tags=["Providers"], status_code=status.HTTP_201_CREATED)
# Definir función para crear un nuevo provider
async def create_new_provider(provider_data: Provider):
    # Llamar a la función del controlador para crear el provider
    result = await create_provider(provider_data)
    # Devolver el resultado de la creación del provider
    return result

# Definir ruta para actualizar un provider existente
@router.put("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
# Definir función para actualizar un provider existente
async def update_existing_provider(provider_data: Provider, id: int):
    # Asignar el ID del provider a los datos del provider
    provider_data.id = id
    # Llamar a la función del controlador para actualizar el provider
    result = await update_provider(provider_data)
    # Devolver el resultado de la actualización del provider
    return result

# Definir ruta para obtener un provider por ID
@router.get("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
# Definir función para obtener un provider por ID
async def get_one_provider_route(id: int):
    # Llamar a la función del controlador para obtener el provider
    result: Provider = await get_one_provider(id)
    # Devolver el provider obtenido
    return result

# Definir ruta para obtener todos los providers
@router.get("/", tags=["Providers"], status_code=status.HTTP_200_OK)
# Definir función para obtener todos los providers
async def get_all_providers_route():
    # Llamar a la función del controlador para obtener todos los providers
    result = await get_all_providers()
    # Devolver la lista de providers obtenida
    return result

# Definir ruta para eliminar un provider por ID
@router.delete("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
# Definir función para eliminar un provider por ID
async def delete_provider_route(id: int):
    # Llamar a la función del controlador para eliminar el provider
    result = await delete_provider(id)
    # Devolver el resultado de la eliminación
    return result