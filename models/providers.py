from pydantic import BaseModel, Field
from typing import Optional
import re

class Provider(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el proveedor"
    )
    
    name: Optional[str] = Field(
        default=None,
        description="El nombre del proveedor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'.-]{1,100}$",
        examples=["Proveedor S.A.", "Distribuciones López"]
    )
    
    phone: Optional[str] = Field(
        default=None,
        description="El número de teléfono del proveedor",
        pattern=r"^\+?[0-9\s-]{7,15}$",
        examples=["+34 123 456 789", "123-456-7890"]
    )
    
    address: Optional[str] = Field(
        default=None,
        description="La dirección del proveedor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s',.-]{1,200}$",
        examples=["Calle Falsa 123, Madrid", "Av. de la Constitución 45, Sevilla"]
    )