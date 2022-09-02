from pinterest import create_app, celery
from pinterest.celery_utils import init_celery

app = create_app()
if __name__ == '__main__':
    init_celery(celery, app)
    app.run()

