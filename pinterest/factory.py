from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pinterest.config import Config
from flask_migrate import Migrate
from flask_mail import Mail
from .celery_utils import init_celery
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'
mail = Mail()

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(app_name=PKG_NAME, **kwargs):
    app = Flask(app_name)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from pinterest.users.routes import users
    from pinterest.pins.routes import pins
    from pinterest.main.routes import main
    from pinterest.admin.routes import admin

    app.register_blueprint(users)
    app.register_blueprint(pins)
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app
