from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask.views import View
from flask_login import current_user, login_required

from pinterest.main.form import SearchForm
from pinterest.pins.form import NewPostForm, UpdatePostForm, NewBoardForm
from pinterest.models import User, Pin, Tags, SavePin, Board, SavePinBoard
from pinterest import db
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
        boards = Board.query.filter_by(user_id=current_user.id).all()
        return render_template('pin.html', title=pin.title, pin=pin, pin_id=pin_id, user=user, boards=boards, form=form)


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


# Un-save pin by user----------------------------------------
class UserUnSavePin(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, pin_id):
        SavePin.query.filter_by(user_id=current_user.id, pin_id=pin_id).delete()
        db.session.commit()
        flash('Pin has been Unsaved.!', 'success')
        return redirect(url_for('users.profile_page'))


pins.add_url_rule('/pin/<int:pin_id>/unsave', view_func=UserUnSavePin.as_view('unsave_pin'))


# create new board-------------------------------------------------
class NewBoard(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self):
        form = NewBoardForm()
        user_save_pins = SavePin.query.filter_by(user_id=current_user.id).all()
        if form.validate_on_submit():
            board = Board(user_id=current_user.id, name=form.name.data)
            db.session.add(board)
            db.session.commit()
            flash('Your board has been created.!', 'success')
            return redirect(url_for('users.profile_page'))

        return render_template('new_board.html', form=form, user_save_pins=user_save_pins)


pins.add_url_rule('/board/new', view_func=NewBoard.as_view('new_board'))


# save pin to board-------------------------------------
class SavePinToBoard(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, board_id, pin_id):
        board = SavePinBoard.query.filter_by(board_id=board_id, pin_id=pin_id).first()
        saved_pin = SavePin.query.filter_by(user_id=current_user.id,pin_id=pin_id).first()
        if board is None:
            pin_save_to_board = SavePinBoard(board_id=board_id, pin_id=pin_id)
            if saved_pin is None:
                save_pin = SavePin(user_id=current_user.id, pin_id=pin_id)
                db.session.add(save_pin)
            db.session.add(pin_save_to_board)
            db.session.commit()
            flash('Pin has been saved into board..!', 'success')
            return redirect(url_for('users.profile_page'))
        else:
            flash('Pin is already saved into This board..!', 'info')
            return redirect(url_for('users.profile_page'))


pins.add_url_rule('/board/<int:board_id>/save/<int:pin_id>', view_func=SavePinToBoard.as_view('save_pin_board'))


# Board info-------------------------------------
class BoardInfo(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, board_id):
        form = SearchForm()
        board_name = Board.query.filter_by(id=board_id).first()
        board = SavePinBoard.query.filter_by(board_id=board_id).all()
        if board == []:
            flash('Your board is empty..!', 'info')
            return render_template('board_details.html', board_name=board_name, board=board, form=form)
        else:
            return render_template('board_details.html', board_name=board_name, board=board, form=form)


pins.add_url_rule('/board/<int:board_id>', view_func=BoardInfo.as_view('board_info'))


# Remove pin from board---------------------------------------
class RemovePinBoard(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, pin_id, board_id):
        SavePinBoard.query.filter_by(pin_id=pin_id, board_id=board_id).delete()
        db.session.commit()
        flash('Your pin has been removed from the board.', 'success')
        return redirect(url_for('pins.board_info', board_id=board_id))


pins.add_url_rule('/board/<int:board_id>/<int:pin_id>/remove', view_func=RemovePinBoard.as_view('remove_pin_board'))


# Delete Board---------------------------------------------------------------
class DeleteBoard(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def dispatch_request(self, board_id):
        SavePinBoard.query.filter_by(board_id=board_id).delete()
        Board.query.filter_by(id=board_id, user_id=current_user.id).delete()
        db.session.commit()
        flash('Board has been successfully deleted.', 'success')
        return redirect(url_for('users.profile_page'))


pins.add_url_rule('/board/<int:board_id>/delete', view_func=DeleteBoard.as_view('delete_board'))
