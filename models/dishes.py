# Definir el modelo Pydantic para Plato
# Define la estructura y validaciones para los datos de platos.
# Importar librerías necesarias
# Librerías para modelos de datos y validaciones
from pydantic import BaseModel, Field
from typing import Optional
import re

# Definir el modelo Pydantic para Plato
class Dish(BaseModel):
    # El ID del plato
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el plato"
    )
    
    # El ID del restaurante al que pertenece el plato
    restaurant_id: Optional[int] = Field(
        default=None,
        description="El ID del restaurante al que pertenece el plato"
    )
    
    # El nombre del plato
    name: Optional[str] = Field(
        default=None,
        description="El nombre del plato",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Spaghetti Carbonara", "Ensalada César"]
    )
    
    # El precio del plato
    price: Optional[float] = Field(
        default=None,
        description="El precio del plato",
        ge=0.0,
        examples=[9.99, 15.50]
    )
    
    # El tipo de plato
    type: Optional[str] = Field(
        default=None,
        description="El tipo de plato (e.g., entrada, plato principal, postre)",
        pattern=r"^(entrada|plato principal|postre|bebida)$",
        examples=["plato principal", "postre"]
    )