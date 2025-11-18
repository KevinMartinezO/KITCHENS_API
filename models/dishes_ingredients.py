# Definir el modelo Pydantic para la relación entre platos e ingredientes
# Define la estructura y validaciones para los datos de platos e ingredientes.
# Importar librerías necesarias
# Librerías para modelos de datos y validaciones
from pydantic import BaseModel, Field
from typing import Optional
import re

# Definir el modelo Pydantic para la relación entre Plato e Ingrediente
class DishIngredient(BaseModel):
    # El ID del plato asociado al ingrediente
    dish_id: Optional[int] = Field(
        default=None,
        description="El ID del plato asociado al ingrediente"
    )
    
    # El nombre del plato asociado al ingrediente
    ingredient_id: Optional[int] = Field(
        default=None,
        description="El ID del ingrediente asociado al plato"
    )
    
    # El nombre del ingrediente asociado al plato
    ingredient_name: Optional[str] = Field(
        default=None,
        description="El nombre del ingrediente asociado al plato",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Tomate", "Queso Mozzarella", "Albahaca"]
    )
    
    # El ID del proveedor asociado al ingrediente
    provider_id: Optional[int] = Field(
        default=None,
        description="El ID del proveedor asociado al ingrediente"
    )
    
    # El nombre del proveedor asociado al ingrediente
    provider_name: Optional[str] = Field(
        default=None,
        description="El nombre del proveedor asociado al ingrediente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Proveedor A", "Proveedor B"]
    )
    
    # El ID del restaurante asociado al plato
    restaurant_id: Optional[int] = Field(
        default=None,
        description="El ID del restaurante asociado al plato"
    )
    
    # El nombre del restaurante asociado al plato
    restaurant_name: Optional[str] = Field(
        default=None,   
        description="El nombre del restaurante asociado al plato",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Pizzería La Bella", "Restaurante El Buen Sabor"]
    )   
    
    # La fecha de disponibilidad del ingrediente para el plato
    availability_date: Optional[str] = Field(
        default=None,   
        description="La fecha de disponibilidad del ingrediente para el plato en formato AAAA-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2024-09-15", "2024-10-01"]
    )
    
    # Indica si el ingrediente está activo para el plato
    active: Optional[bool] = Field(
        default=None,
        description="Indica si el ingrediente está activo para el plato"
    )