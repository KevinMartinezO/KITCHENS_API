from pydantic import BaseModel, Field
from typing import Optional
import re

class Restaurant(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el restaurante"
    )
    
    name: Optional[str] = Field(
        default=None,
        description="El nombre del restaurante",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]{1,100}$",
        examples=["La Casa de las Empanadas", "Pizzería El Buen Sabor"]
    )
    
    address: Optional[str] = Field(
        default=None,
        description="La dirección del restaurante",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s',.-]{1,200}$",
        examples=["Calle Falsa 123, Ciudad", "Avenida Siempre Viva 742, Pueblo"]
    )   
    
    phone: Optional[str] = Field(
        default=None,
        description="El número de teléfono del restaurante",
        pattern=r"^\+?[0-9\s-]{7,15}$",
        examples=["+34 123 456 789", "123-456-7890"]
    )   
    