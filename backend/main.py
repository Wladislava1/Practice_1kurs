from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Для парсинга вакансий и записи в БД
@app.post("/parse_job/")
def parse_job(job_request: schemas.JobRequest, db: Session = Depends(database.get_db)):
    return crud.parse_and_store_job(job_request, db)


# Список вакансий с фильтрацией
@app.get("/jobs/")
def get_jobs(db: Session = Depends(database.get_db), filters: dict = None):
    return crud.get_jobs(db, filters)


