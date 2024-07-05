from pydantic import BaseModel
from typing import Optional

class JobRequest(BaseModel): # данные от пользователя (post - запрос)
    title: str  # Название
    schedule: Optional[str] = None  # График работы
    salary: Optional[int] = None  # Зарплата
    experience: Optional[str] = None  # Опыт работы

class JobResponse(BaseModel): # данные для пользователя (get - запрос)
    id: int
    title: str
    schedule: str
    salary: int
    experience: str

    class Config:
        orm_mode = True