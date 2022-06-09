from pinterest import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# models----------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False , default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    pins = db.relationship('Pin', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow )
    pin_pic = db.Column(db.String(500), nullable=False, default='default.jpg')
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Pin('{self.title}','{self.date_posted}')"

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Tags('{self.name}')"

class UserInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

    def __repr__(self):
        return f"Tags('{self.user_id}','{self.tag_id}')"
