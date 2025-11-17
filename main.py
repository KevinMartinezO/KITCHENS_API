import uvicorn
from fastapi import FastAPI
from routes.restaurants import router as router_restaurant
from routes.dishes import router as router_dish
from routes.ingredients import router as router_ingredient
from routes.providers import router as router_provider

app = FastAPI()

app.include_router(router_restaurant)
app.include_router(router_dish)
app.include_router(router_ingredient)
app.include_router(router_provider)


@app.get("/")
def read_root():
    return {
        "Hello": "KITCHENS_API",
        "version": "0.0.1"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")