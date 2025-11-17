from pydantic import BaseModel, Field
from typing import Optional
import re

class Ingredient(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el ingrediente"
    )
    
    provider_id: Optional[int] = Field(
        default=None,
        description="El ID del proveedor al que pertenece el ingrediente"
    )
    
    name: Optional[str] = Field(
        default=None,
        description="El nombre del ingrediente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["Tomate", "Queso Manchego"]
    )
    
    category: Optional[str] = Field(
        default=None,
        description="La categoría del ingrediente (e.g., vegetal, lácteo, carne)",
        pattern=r"^(vegetal|lácteo|carne|grano|fruta|otro)$",
        examples=["vegetal", "lácteo"]
    )   