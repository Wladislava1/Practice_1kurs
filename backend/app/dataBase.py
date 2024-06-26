from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db:5432/job_parser"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # Движок БД  для установления соединений с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Изменения в сессии не будут автоматически фиксироваться и сбрасываться

Base = declarative_base()

def get_db():
    db = SessionLocal() # Создание новой сессии БД
    try:
        yield db
    finally:
        db.close()  # Сессия будет закрыта после завершения запроса