from pinterest import celery
from pinterest.factory import create_app
from pinterest.celery_utils import init_celery

app = create_app()
init_celery(celery, app)
