### To Start Celery Worker

- Command :- `celery -A celery_worker.celery worker -l info`

### To Start Celery Beat (Task Scheduling)

- Command :- ` celery -A celery_worker.celery beat -l info`

### To run flower

- Command :- `celery -A celery_worker.celery flower`

### Referred Blog for celery beat

- link : `https://medium.com/@channeng/setting-up-a-task-scheduler-application-with-celery-flask-part-1-8652265050dc`

### Referred Blog for celery

- link : `https://medium.com/@frassetto.stefano/flask-celery-howto-d106958a15fe`

