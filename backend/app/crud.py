import requests
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional

#  Получение вакансий с hh.ru
def fetch_jobs_from_hh(query: str):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': query,
        'per_page': 100 # Количество результатов на странице
    }
    if schedule:
        params['schedule'] = schedule
    if salary:
        params['salary'] = salary
    if experience:
        params['experience'] = experience
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items']

# Парсинг и сохранение вакансий в базу данных
def parse_and_store_job(job_request: schemas.JobRequest, db: Session):
    hh_jobs = fetch_jobs_from_hh(job_request.title, job_request.schedule, job_request.salary, job_request.experience)
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
    
    for job in jobs:
        print(job, job.title)
    return jobs

# Получение списка вакансий с фильтрацией
def get_jobs(
    db: Session, 
    salary: Optional[str] = None,
    experience: Optional[str] = None,
    schedule: Optional[str] = None,
    title: Optional[str] = None,
     limit: int = 100,
    offset: int = 0
    ):
    query = db.query(models.Job)
    if schedule not in ('',None):
        query = query.filter(models.Job.schedule == schedule)
    if salary not in ('',None):
        query = query.filter(models.Job.salary == salary)
    if experience not in ('',None):
        query = query.filter(models.Job.experience == experience)
    if title not in ('',None):
        query = query.filter(models.Job.title.ilike(f"%{title}%"))

    jobs = query.offset(offset).limit(limit).all()
    return jsonable_encoder(jobs)