### To Start Celery Worker

- Command :- `celery -A celery_worker.celery worker -l info`

### To Start Celery Beat (Task Scheduling)

- Command :- ` celery -A celery_worker.celery beat -l info`

### To run flower

- Command :- `celery -A celery_worker.celery flower`

