from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'
mail = Mail()
celery = Celery('pinterest', broker="redis://localhost:6379/1", backend="redis://localhost:6379/0")


def create_app(config_class=Config):
    """
    create app
    :param config_class: configurations
    :return: app
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.info("app configuration is set.")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # register blueprints
    from pinterest.users.routes import users
    from pinterest.pins.routes import pins
    from pinterest.main.routes import main
    from pinterest.admin.routes import admin
    from pinterest.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(pins)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app
