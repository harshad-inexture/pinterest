from pinterest import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User's models----------------------------------------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    pins = db.relationship('Pin', backref='author', cascade="all,delete")
    like = db.relationship('Like', backref='user', cascade="all,delete")
    follow = db.relationship('Follow', backref='user', cascade="all,delete")
    comments = db.relationship('Comment', backref='user', cascade="all,delete")

    def get_reset_token(self, expires_sec=900):
        s = Serializer(app.secret_key, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}',{self.profile_pic},{self.id})"


class UserInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

    def __repr__(self):
        return f"User Tags('{self.user_id}','{self.tag_id}')"


# Pin's models------------------------------------------------------------------------------
class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pin_pic = db.Column(db.String(50), nullable=False, default='default.jpg')
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    privacy = db.Column(db.Integer, nullable=False)

    user_save_pins = db.relationship('SavePin', backref='save_pins', cascade="all,delete")
    user_save_pins_board = db.relationship('SavePinBoard', backref='save_pins_board', cascade="all,delete")
    like = db.relationship('Like', backref='pin', cascade="all,delete")
    pin_tags = db.relationship('PinTags', backref='pin', cascade="all,delete")
    comments = db.relationship('Comment', backref='pin', cascade="all,delete")

    def __repr__(self):
        return f"Pin('{self.pin_pic}','{self.title}','{self.date_posted}','{self.content}')"


class PinTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id', ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

    def __repr__(self):
        return f"PinTags('{self.pin_id}','{self.tag_id}')"


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Tags('{self.name}')"


class SavePin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Save Pins('{self.user_id}','{self.pin_id}')"


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    privacy = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Save Board('{self.id}','{self.user_id}','{self.name}','{self.privacy}')"


class SavePinBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Save Pins To Board('{self.board_id}','{self.pin_id}')"


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id', ondelete='CASCADE'), nullable=False)


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    pin_id = db.Column(db.Integer, db.ForeignKey('pin.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
