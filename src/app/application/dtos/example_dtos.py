from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExampleCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Example name")
    description: Optional[str] = Field(None, description="Example description")

class ExampleUpdateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Example name")
    description: Optional[str] = Field(None, description="Example description")

class ExampleResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
