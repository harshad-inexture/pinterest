from pinterest import app
import secrets, os
from PIL import Image

def save_pin_img(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pin_pic_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pin_img', pin_pic_fn)

    i = Image.open(form_pic)
    i.save(picture_path)
    return pin_pic_fn