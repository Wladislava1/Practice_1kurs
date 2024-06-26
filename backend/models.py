from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True) 
    title = Column(String, index=True) # Название
    schedule = Column(String, index=True) # Расписание
    salary = Column(String, index=True) # Зарплата
    experience = Column(String, index=True) # Опыт работы
