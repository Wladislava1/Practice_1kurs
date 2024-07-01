from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Главная страница, возвращающая index.html
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# CORS middleware для разрешения доступа с локального хоста
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["POST", "GET"], 
    allow_headers=["*"],
)

# Для парсинга вакансий и записи в БД
@app.post("/parse_job/")
def parse_job(job_request: schemas.JobRequest, db: Session = Depends(database.get_db)):
    print(job_request.title)
    jobs = crud.parse_and_store_job(job_request, db)
    for job in jobs:
        print(job, job.title)
    return jobs 

# Список вакансий с фильтрацией
@app.get("/jobs/")
def get_jobs(db: Session = Depends(database.get_db), filters: dict = None):
    return crud.get_jobs(db, filters)



