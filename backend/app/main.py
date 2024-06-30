from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Подключение статических файлов из frontend/static/
app.mount("/static", StaticFiles(directory="/static/"), name="static")

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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Обработчики для вашего API

# Для парсинга вакансий и записи в БД
@app.post("/parse_job/")
def parse_job(job_request: schemas.JobRequest, db: Session = Depends(database.get_db)):
    return crud.parse_and_store_job(job_request, db)

# Список вакансий с фильтрацией
@app.get("/jobs/")
def get_jobs(db: Session = Depends(database.get_db), filters: dict = None):
    return crud.get_jobs(db, filters)



