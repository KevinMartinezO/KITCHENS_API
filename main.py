# Main punto de entrada para la API de KITCHENS_API
# Configura y ejecuta la aplicación FastAPI, incluyendo las rutas necesarias.
import uvicorn
from fastapi import FastAPI
# Importar routers de las diferentes rutas
from routes.restaurants import router as router_restaurant
from routes.dishes import router as router_dish
from routes.ingredients import router as router_ingredient
from routes.providers import router as router_provider

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Incluir los routers en la aplicación
app.include_router(router_restaurant)
app.include_router(router_dish)
app.include_router(router_ingredient)
app.include_router(router_provider)

# Definir la ruta raíz para verificar que la API está funcionando
@app.get("/")
# Ruta raíz que devuelve un mensaje de bienvenida y la versión de la API
def read_root():
    # Devuelve un mensaje de bienvenida y la versión de la API
    return {
        "Hello": "KITCHENS_API",
        "version": "0.2.0"
    }

# Ejecutar la aplicación si este archivo es el punto de entrada principal
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")