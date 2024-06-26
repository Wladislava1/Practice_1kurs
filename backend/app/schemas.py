from pydantic import BaseModel

class JobRequest(BaseModel): # данные от пользователя (post - запрос)
    title: str # Название
    schedule: str # График работы
    salary: int # Зарплата
    experience: str # Опыт работы

class JobResponse(BaseModel): # данные для пользователя (get - запрос)
    id: int
    title: str
    schedule: str
    salary: int
    experience: str

    class Config:
        orm_mode = True