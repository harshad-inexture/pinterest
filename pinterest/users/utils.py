from pinterest import app
import secrets, os
from PIL import Image
from wtforms.validators import ValidationError

def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    profile_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_img', profile_fn)

    pic_size = (150, 150)
    i = Image.open(form_pic)
    i.thumbnail(pic_size)

    i.save(picture_path)
    return profile_fn

def selected_user_tags(user_tags):
    selected_tags = []
    for i in user_tags:
        selected_tags.append(i.tag_id)
    return selected_tags


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']

    if not any(char.isdigit() for char in passwd):
        msg = 'Password should have at least one numeral'
        return True,msg

    elif not any(char.isupper() for char in passwd):
        msg = 'Password should have at least one uppercase letter'
        return True,msg

    elif not any(char.islower() for char in passwd):
        msg = 'Password should have at least one lowercase letter'
        return True,msg

    elif not any(char in SpecialSym for char in passwd):
        msg = 'Password should have at least one of the symbols $@#'
        return True,msg

    else:
        msg = 'Password validate'
        return False,msg