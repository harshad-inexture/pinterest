from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pinterest.config import Config
from flask_migrate import Migrate

app = Flask(__name__)

# configs---------------------------------------------------------------------------------
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='users.login_page'
login_manager.login_message_category='info'

from pinterest.users.routes import users
from pinterest.pins.routes import pins
from pinterest.main.routes import main

app.register_blueprint(users)
app.register_blueprint(pins)
app.register_blueprint(main)
