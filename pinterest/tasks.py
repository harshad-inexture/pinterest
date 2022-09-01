from pinterest import celery
from flask_mail import Message
from pinterest import mail


@celery.task()
def send_reset_email(user_email, user_token):
    msg = Message('Password Reset Request', sender='inexture@gmail.com', recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@celery.task()
def print_hello():
    print(f"New Post")
