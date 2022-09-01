# How To Configure Celery Using Flask

***
We are going to integrate celery in our flask app.

- Please first go with the flask celery integration
  documentation [Flask+Celery](https://flask.palletsprojects.com/en/2.2.x/patterns/celery/).
- So You start with small application and everything looks pretty neat: you’ve created your app instance, made a Celery
  app with it and
  wrote some tasks to call in your route handlers. Things are doing great, your app’s growing and you’ve decided to
  embrace
  the [application factories’](https://flask.palletsprojects.com/en/1.0.x/patterns/appfactories/#application-factories)
  Flask approach to gain more flexibility, but you’re not too sure on how to maintain
  Celery nice and clean inside your app.
- Moreover, you’ll want to isolate all your tasks definitions in a sub-folder to import them in your views, blueprints,
  flask-restful Resources, or anywhere you may need to.
- The problem, though, is that if you stick to the old pattern it will be impossible for you to import your celery
  instance inside other modules, now that it lives inside your create_app() function. This approach could get daunting,
  as it’s very likely to run into circular imports.
- Flask documentation’s pretty clear on how to deal with (factories and
  extensions)[https://flask.palletsprojects.com/en/1.0.x/patterns/appfactories/#factories-extensions]: It’s preferable
  to create your
  extensions and app factories so that the extension object does not initially get bound to the application.
- In our case this means splitting our make_celery() function in two different ones:\
  1). The first creating a Celery app instance \
  2). Performing the tasks needed to bind that exact instance to the Flask app.

***

- First we are creating celery app instance in our application package (`pinterest/__init__.py`).

```python
from celery import Celery

celery = Celery('pinterest', broker="redis://localhost:6379/1", backend="redis://localhost:6379/0")
```

***

- Performing the tasks needed to bind that exact instance to the Flask app.

    - For that we are creating on file name `pinterest\celery_utils.py`.
    - modified make_celery() function.

```python
def init_celery(celery, app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
```

***

- Now, in our flask app entrypoint(`app.py`)

```python
from pinterest import create_app, celery
from pinterest.celery_utils import init_celery

app = create_app()
init_celery(celery, app)
```

- Now we can import celery app instance in other modules.
- For all the task we create `pinterest\tasks.py` file. In that file, all our background task methods and functions are
  their. To define in celery task queue we are using `@celery.task()` decorator to the function.
- For example:-
```python
@celery.task()
def print_hello():
    print(f"New Post")
```

- Then the Flask application can request the execution of this background task as follows:
```python
result = print_hello.delay()
```
***

# Celery-beat configuration for task scheduling

- For the celery beat configuration we add `CeleryConfig` configuration class in our flask app `config.py` file.

```python
class CeleryConfig:
    imports = ('pinterest.tasks')
    timezone = 'UTC'

    accept_content = ['json', 'msgpack', 'yaml']
    task_serializer = 'json'
    result_serializer = 'json'

    beat_schedule = {
        'test-celery': {
            'task': 'pinterest.tasks.print_hello',
            'schedule': timedelta(seconds=10),
        }
    }
```
- And update celery configs in our `celery_utils.py` file.

Updated **celery_utils.py**

```python
from config import CeleryConfig


def init_celery(celery, app):
    celery.conf.update(app.config)
    celery.config_from_object(CeleryConfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

```

***

### To Start Celery Worker

- Command :- `celery -A app(celery_app_name).celery worker -l info`

### To Start Celery Beat (Task Scheduling)

- Command :- ` celery -A app(celery_app_name).celery beat -l info`

### To run flower

- Command :- `celery -A app(celery_app_name).celery flower`

### Referred Blog for celery beat

- link : `https://medium.com/@channeng/setting-up-a-task-scheduler-application-with-celery-flask-part-1-8652265050dc`

### Referred Blog for celery

- link : `https://medium.com/@frassetto.stefano/flask-celery-howto-d106958a15fe`

