from flask import Blueprint
from flask.views import View
from flask import render_template, flash, redirect, url_for, request, abort

from pinterest.main.form import SearchForm
from pinterest.pins.form import NewPostForm, UpdatePostForm
from pinterest.models import User, Pin, Tags, SavePin
from pinterest import db
from flask_login import current_user, login_required
from pinterest.pins.utils import save_pin_img

pins = Blueprint('pins', __name__)


# @pins.route("/pin/new", methods=['POST', 'GET'])
# @login_required
# def new_pin():
#     form = NewPostForm()
#     tags = Tags.query.all()
#     if form.validate_on_submit():
#         if form.post_img.data:
#             pin_pic = save_pin_img(form.post_img.data)
#             pin = Pin(title=form.title.data, pin_pic=pin_pic, content=form.content.data, tag=form.img_tag.data,
#                       user_id=current_user.id)
#             db.session.add(pin)
#             db.session.commit()
#             flash('Your post has been created...!!!', 'success')
#             return redirect(url_for('main.home_page'))
#     return render_template('new_post.html', title='New Post', form=form, tags=tags)


class NewPin(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self):
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


pins.add_url_rule('/pin/new', view_func=NewPin.as_view('new_pin'))


# @pins.route("/pin/<int:pin_id>")
# def selected_pin(pin_id):
#     pin = Pin.query.get_or_404(pin_id)
#     user = User.query.get_or_404(pin.user_id)
#     return render_template('pin.html', title=pin.title, pin=pin, user=user)

class SelectedPin(View):

    def dispatch_request(self, pin_id):
        form = SearchForm()
        pin = Pin.query.get_or_404(pin_id)
        user = User.query.get_or_404(pin.user_id)
        return render_template('pin.html', title=pin.title, pin=pin, pin_id=pin_id, user=user, form=form)


pins.add_url_rule('/pin/<int:pin_id>', view_func=SelectedPin.as_view('selected_pin'))


# @pins.route("/pin/<int:pin_id>/update", methods=['POST', 'GET'])
# @login_required
# def update_pin(pin_id):
#     pin = Pin.query.get_or_404(pin_id)
#     user = User.query.get_or_404(pin.user_id)
#     form = UpdatePostForm()
#     tags = Tags.query.all()
#     if pin.author != current_user:
#         abort(403)
#     if form.validate_on_submit():
#         pin.title = form.title.data
#         pin.content = form.content.data
#         pin.tag = form.img_tag.data
#         db.session.commit()
#         flash('Your pin has been updated.!', 'success')
#         return redirect(url_for('pins.update_pin', pin_id=pin.id))
#     if request.method == 'GET':
#         form.title.data = pin.title
#         form.content.data = pin.content
#
#     return render_template('update_pin.html', title=pin.title, pin=pin, user=user, form=form, tags=tags)

class UpdatePin(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, pin_id):
        pin = Pin.query.get_or_404(pin_id)
        user = User.query.get_or_404(pin.user_id)
        form = UpdatePostForm()
        tags = Tags.query.all()
        if pin.author != current_user:
            abort(403)
        if form.validate_on_submit():
            pin.title = form.title.data
            pin.content = form.content.data
            pin.tag = form.img_tag.data
            db.session.commit()
            flash('Your pin has been updated.!', 'success')
            return redirect(url_for('pins.update_pin', pin_id=pin.id))
        if request.method == 'GET':
            form.title.data = pin.title
            form.content.data = pin.content

        return render_template('update_pin.html', title=pin.title, pin=pin, user=user, form=form, tags=tags)


pins.add_url_rule("/pin/<int:pin_id>/update", view_func=UpdatePin.as_view('update_pin'))


# @pins.route("/pin/<int:pin_id>/delete", methods=['POST'])
# @login_required
# def delete_pin(pin_id):
#     pin = Pin.query.get_or_404(pin_id)
#     if pin.author != current_user:
#         abort(403)
#     db.session.delete(pin)
#     db.session.commit()
#     flash('Your pin has been deleted.!', 'success')
#     return redirect(url_for('users.profile_page'))

class DeletePin(View):
    methods = ['POST']
    decorators = [login_required]

    def dispatch_request(self, pin_id):
        pin = Pin.query.get_or_404(pin_id)
        if pin.author != current_user:
            abort(403)
        db.session.delete(pin)
        db.session.commit()
        flash('Your pin has been deleted.!', 'success')
        return redirect(url_for('users.profile_page'))


pins.add_url_rule('/pin/<int:pin_id>/delete', view_func=DeletePin.as_view('delete_pin'))


class UserSavePin(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, pin_id):
        pin = SavePin.query.filter_by(pin_id=pin_id).first()
        if pin is None:
            save_pin = SavePin(user_id=current_user.id, pin_id=pin_id)
            db.session.add(save_pin)
            db.session.commit()
            flash('Pin has been saved.!', 'success')
            return redirect(url_for('users.profile_page'))
        else:
            flash('Pin is already saved.!', 'info')
            return redirect(url_for('users.profile_page'))


pins.add_url_rule('/pin/<int:pin_id>/save', view_func=UserSavePin.as_view('save_pin'))
