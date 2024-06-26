import requests
from sqlalchemy.orm import Session
from . import models, schemas

#  Получение вакансий с hh.ru
def fetch_jobs_from_hh(query: str):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': query,
        'per_page': 200  # Количество результатов на странице
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items']

# Парсинг и сохранение вакансий в базу данных
def parse_and_store_job(job_request: schemas.JobRequest, db: Session):
    hh_jobs = fetch_jobs_from_hh(job_request.title)
    jobs = []
    
    for hh_job in hh_jobs:
        # Создание объектов модели Job для каждой вакансии и сохранение их в базе данных
        job = models.Job(
            title=hh_job.get('name'),
            schedule=hh_job.get('schedule', {}).get('name', ''),
            salary=hh_job.get('salary', {}).get('from', 0) if hh_job.get('salary') else 0,
            experience=hh_job.get('experience', {}).get('name', '')
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        jobs.append(job)
    
    return jobs

# Получение списка вакансий с фильтрацией
def get_jobs(db: Session, filters: dict):
    query = db.query(models.Job)
    if filters:
        if filters.get("schedule"):
            query = query.filter(models.Job.schedule == filters["schedule"])
        if filters.get("salary"):
            query = query.filter(models.Job.salary >= filters["salary"])
        if filters.get("experience"):
            query = query.filter(models.Job.experience == filters["experience"])
    return query.all()
