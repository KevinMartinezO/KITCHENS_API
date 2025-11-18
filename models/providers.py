# Definir el modelo Pydantic para Proveedor
# Define la estructura y validaciones para los datos de proveedores.
# Importar librerías necesarias
# Librerías para modelos de datos y validaciones
from pydantic import BaseModel, Field
from typing import Optional
import re

# Definir el modelo Pydantic para Proveedor
class Provider(BaseModel):
    # El ID del proveedor
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el proveedor"
    )
    
    # El nombre del proveedor
    name: Optional[str] = Field(
        default=None,
        description="El nombre del proveedor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'.-]{1,100}$",
        examples=["Proveedor S.A.", "Distribuciones López"]
    )
    
    # El número de teléfono del proveedor
    phone: Optional[str] = Field(
        default=None,
        description="El número de teléfono del proveedor",
        pattern=r"^\+?[0-9\s-]{7,15}$",
        examples=["+34 123 456 789", "123-456-7890"]
    )
    
    # La dirección del proveedor
    address: Optional[str] = Field(
        default=None,
        description="La dirección del proveedor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s',.-]{1,200}$",
        examples=["Calle Falsa 123, Madrid", "Av. de la Constitución 45, Sevilla"]
    )