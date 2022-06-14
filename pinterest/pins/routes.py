from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request,abort
from pinterest.pins.form import NewPostForm, UpdatePostForm
from pinterest.models import User, Pin, Tags
from pinterest import db
from flask_login import current_user,login_required
from pinterest.pins.utils import save_pin_img

pins = Blueprint('pins',__name__)

@pins.route("/pin/new", methods=['POST', 'GET'])
@login_required
def new_pin():
    form = NewPostForm()
    tags = Tags.query.all()
    if form.validate_on_submit():
        if form.post_img.data:
            pin_pic = save_pin_img(form.post_img.data)
            pin = Pin(title=form.title.data, pin_pic=pin_pic, content=form.content.data, tag=form.img_tag.data,
                      user_id=current_user.id)
            db.session.add(pin)
            db.session.commit()
            flash('Your post has been created...!!!', 'success')
            return redirect(url_for('main.home_page'))
    return render_template('new_post.html', title='New Post', form=form, tags=tags)

@pins.route("/pin/<int:pin_id>")
def selected_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get_or_404(pin.user_id)
    return render_template('pin.html',title=pin.title,pin=pin,user=user)

@pins.route("/pin/<int:pin_id>/update", methods=['POST', 'GET'])
@login_required
def update_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    user = User.query.get_or_404(pin.user_id)
    form = UpdatePostForm()
    tags = Tags.query.all()
    if pin.author != current_user:
        abort(403)
    if form.validate_on_submit():
        pin.title=form.title.data
        pin.content=form.content.data
        pin.tag=form.img_tag.data
        db.session.commit()
        flash('Your pin has been updated.!', 'success')
        return redirect(url_for('pins.update_pin',pin_id=pin.id))
    if request.method == 'GET':
        form.title.data = pin.title
        form.content.data = pin.content

    return render_template('update_pin.html',title=pin.title,pin=pin,user=user,form=form,tags=tags)

@pins.route("/pin/<int:pin_id>/delete", methods=['POST'])
@login_required
def delete_pin(pin_id):
    pin = Pin.query.get_or_404(pin_id)
    if pin.author != current_user:
        abort(403)
    db.session.delete(pin)
    db.session.commit()
    flash('Your pin has been deleted.!', 'success')
    return redirect(url_for('users.profile_page'))