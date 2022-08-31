from pinterest import create_app
from pinterest.factory import celery

if __name__ == '__main__':
    app = create_app(celery=celery)
    app.run()
