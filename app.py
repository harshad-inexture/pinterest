from pinterest import create_app, celery
from pinterest.celery_utils import init_celery

# if __name__ == '__main__':
#     app = create_app()
#     init_celery(celery, app)
#     app.run()

app = create_app()
init_celery(celery, app)

