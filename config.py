import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(seconds=20)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')


class CeleryConfig:
    imports = ('pinterest.tasks')
    timezone = 'UTC'

    accept_content = ['json', 'msgpack', 'yaml']
    task_serializer = 'json'
    result_serializer = 'json'

    beat_schedule = {
        'test-celery': {
            'task': 'pinterest.tasks.print_hello',
            # Every minute
            'schedule': timedelta(seconds=10),
        }
    }
