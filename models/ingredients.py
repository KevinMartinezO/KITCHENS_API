# Definir el modelo Pydantic para Ingrediente
# Define la estructura y validaciones para los datos de ingredientes.
# Importar librerías necesarias
# Librerías para modelos de datos y validaciones
from pydantic import BaseModel, Field
from typing import Optional
import re

# Definir el modelo Pydantic para Ingrediente
class Ingredient(BaseModel):
    # El ID del ingrediente
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el ingrediente"
    )
    
    # El ID del proveedor al que pertenece el ingrediente
    provider_id: Optional[int] = Field(
        default=None,
        description="El ID del proveedor al que pertenece el ingrediente"
    )
    
    # El nombre del ingrediente
    name: Optional[str] = Field(
        default=None,
        description="El nombre del ingrediente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Tomate", "Queso Manchego"]
    )
    
    # La categoría del ingrediente
    category: Optional[str] = Field(
        default=None,
        description="La categoría del ingrediente (e.g., vegetal, lácteo, carne)",
        pattern=r"^(vegetal|lácteo|carne|grano|fruta|otro)$",
        examples=["vegetal", "lácteo"]
    )   