from pydantic import BaseModel, Field
from typing import Optional
import re

class DishIngredient(BaseModel):
    dish_id: Optional[int] = Field(
        default=None,
        description="El ID del plato asociado al ingrediente"
    )
    
    ingredient_id: Optional[int] = Field(
        default=None,
        description="El ID del ingrediente asociado al plato"
    )
    
    ingredient_name: Optional[str] = Field(
        default=None,
        description="El nombre del ingrediente asociado al plato",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Tomate", "Queso Mozzarella", "Albahaca"]
    )
    
    provider_id: Optional[int] = Field(
        default=None,
        description="El ID del proveedor asociado al ingrediente"
    )
    
    provider_name: Optional[str] = Field(
        default=None,
        description="El nombre del proveedor asociado al ingrediente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Proveedor A", "Proveedor B"]
    )
    
    restaurant_id: Optional[int] = Field(
        default=None,
        description="El ID del restaurante asociado al plato"
    )
    
    restaurant_name: Optional[str] = Field(
        default=None,   
        description="El nombre del restaurante asociado al plato",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Pizzería La Bella", "Restaurante El Buen Sabor"]
    )   
    
    availability_date: Optional[str] = Field(
        default=None,   
        description="La fecha de disponibilidad del ingrediente para el plato en formato AAAA-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2024-09-15", "2024-10-01"]
    )
    
    active: Optional[bool] = Field(
        default=None,
        description="Indica si el ingrediente está activo para el plato"
    )