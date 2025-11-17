from fastapi import APIRouter, status
from models.providers import Provider
from controllers.providers import(
    create_provider,
    update_provider,
    get_one_provider,
    get_all_providers,
    delete_provider
)

router = APIRouter(prefix="/providers")

@router.post("/", tags=["Providers"], status_code=status.HTTP_201_CREATED)
async def create_new_provider(provider_data: Provider):
    result = await create_provider(provider_data)
    return result

@router.put("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
async def update_existing_provider(provider_data: Provider, id: int):
    provider_data.id = id
    result = await update_provider(provider_data)
    return result

@router.get("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
async def get_one_provider_route(id: int):
    result: Provider = await get_one_provider(id)
    return result

@router.get("/", tags=["Providers"], status_code=status.HTTP_200_OK)
async def get_all_providers_route():
    result = await get_all_providers()
    return result

@router.delete("/{id}", tags=["Providers"], status_code=status.HTTP_200_OK)
async def delete_provider_route(id: int):
    result = await delete_provider(id)
    return result