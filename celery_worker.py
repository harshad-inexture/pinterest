from pinterest.factory import celery
from pinterest import create_app
from pinterest.celery_utils import init_celery

app = create_app()
init_celery(celery, app)
