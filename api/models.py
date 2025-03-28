from db.models import MiniTest  # Переиспользуем уже существующую модель

#Pydantic-модель для сериализации ответа:
from pydantic import BaseModel

class MiniTestResponse(BaseModel):
    id: int
    onn: bool

    class Config:
        from_attributes = True  # для FastAPI >=0.100.0