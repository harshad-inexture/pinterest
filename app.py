from pinterest.factory import create_app
import pinterest

if __name__ == '__main__':
    app = create_app(celery=pinterest.celery)
    app.run()
