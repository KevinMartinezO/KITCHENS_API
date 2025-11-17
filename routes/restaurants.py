from fastapi import APIRouter, status
from models.restaurants import Restaurant
from controllers.restaurants import(
    create_restaurant,
    update_restaurant,
    get_one_restaurant,
    get_all_restaurants,
    delete_restaurant
)

router = APIRouter(prefix="/restaurants")

@router.post("/", tags=["Restaurants"], status_code=status.HTTP_201_CREATED)
async def create_new_restaurant(restaurant_data: Restaurant):
    result = await create_restaurant(restaurant_data)
    return result

@router.put("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
async def update_existing_restaurant(restaurant_data: Restaurant, id: int):
    restaurant_data.id = id
    result = await update_restaurant(restaurant_data)
    return result

@router.get("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
async def get_one_restaurant_route(id: int):
    result: Restaurant = await get_one_restaurant(id)
    return result

@router.get("/", tags=["Restaurants"], status_code=status.HTTP_200_OK)
async def get_all_restaurants_route():
    result = await get_all_restaurants()
    return result

@router.delete("/{id}", tags=["Restaurants"], status_code=status.HTTP_200_OK)
async def delete_restaurant_route(id: int):
    result = await delete_restaurant(id)
    return result