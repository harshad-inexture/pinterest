from flask import Blueprint, render_template, flash, redirect, url_for
from pinterest.main.form import SearchForm
from flask_login import current_user, login_required
from pinterest.models import Tags, User, Board, Pin, BlockUser
from pinterest import db
from pinterest.admin.utils import block_user_list
from pinterest.admin.form import UpdateTagForm, BlockUserMsg
from pinterest.msg import ADMIN_ACCESS_MSG, USER_NOT_EXIST_MSG, ADMIN_UPDATE_TAG_MSG,ADMIN_NEW_TAG_MSG ,ADMIN_DELETE_TAG_MSG, \
    ADMIN_TAG_NOT_EXIST_MSG, ADMIN_BLOCK_MSG, ADMIN_UNBLOCK_MSG

admin = Blueprint('admin', __name__)


@admin.route("/admin", methods=['POST', 'GET'])
@login_required
def admin_page():
    """Admin home page.
    only admin can access this page.
    :return: details about tags,pin and user
    """

    id = current_user.id
    if id == 1:
        form = SearchForm()
        tags = Tags.query.all()
        users = User.query.all()
        blocks = BlockUser.query.all()
        block_list = block_user_list(blocks)
        return render_template('admin.html', tags=tags, form=form, users=users, block_list=block_list)
    else:
        flash(ADMIN_ACCESS_MSG, 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/tags/new", methods=['POST', 'GET'])
@login_required
def admin_new_tag():
    """create new pin tag.
    :return: admin home page
    """

    id = current_user.id
    if id == 1:
        form = UpdateTagForm()
        if form.validate_on_submit():
            if tag := Tags.query.filter_by(name=form.name.data).first():
                flash('Tag is already exist...!!!', 'warning')
            else:
                new_tag = Tags(name=form.name.data)
                db.session.add(new_tag)
                db.session.commit()

                flash(ADMIN_NEW_TAG_MSG, 'success')
            return redirect(url_for('admin.admin_page'))
        return render_template('admin_new_tag.html', form=form)
    else:
        flash(ADMIN_ACCESS_MSG, 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/tags/<int:tag_id>/update", methods=['POST', 'GET'])
@login_required
def admin_tag_update(tag_id):
    """update tag route
    :param tag_id: 'integer'
    :return: admin home page with updated tag.
    """

    id = current_user.id
    if id == 1:
        tag = Tags.query.filter_by(id=tag_id).first()
        form = UpdateTagForm()
        if tag is not None:
            if form.validate_on_submit():
                tag.name = form.name.data
                db.session.commit()
                flash(ADMIN_UPDATE_TAG_MSG, 'success')
                return redirect(url_for('admin.admin_page'))
            return render_template('admin_update_tag.html', form=form, tag=tag)
        else:
            flash(ADMIN_TAG_NOT_EXIST_MSG, 'warning')
            return redirect(url_for('admin.admin_page'))
    else:
        flash(ADMIN_ACCESS_MSG, 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/tags/<int:tag_id>/delete", methods=['GET'])
@login_required
def admin_tag_delete(tag_id):
    """delete tag route.
    :param tag_id: 'integer'
    :return: admin home page and delete tag.
    """

    id = current_user.id
    if id == 1:
        tag = Tags.query.filter_by(id=tag_id)
        if tag is not None:
            tag.delete()
            db.session.commit()
            flash(ADMIN_DELETE_TAG_MSG, 'success')
        else:
            flash(admin_tag_not_exist, 'warning')
        return redirect(url_for('admin.admin_page'))
    else:
        flash(ADMIN_TAG_NOT_EXIST_MSG, 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/user/<int:user_id>", methods=['POST', 'GET'])
@login_required
def admin_user_details(user_id):
    """admin can see user details.
    """

    id = current_user.id
    if id == 1:
        form = SearchForm()
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            boards = Board.query.filter_by(user_id=user_id).all()
            pins = Pin.query.filter_by(user_id=user_id).all()
            return render_template('admin_user_page.html', boards=boards, pins=pins, user=user, form=form)
        else:
            flash(USER_NOT_EXIST_MSG, 'warning')
            return redirect(url_for('admin.admin_page'))
    else:
        flash(admin_access_msg, 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/user/<int:user_id>/block", methods=['POST', 'GET'])
@login_required
def admin_block_user(user_id):
    """admin can see user details and block and unblock them.
    """

    id = current_user.id
    if id == 1:
        user = User.query.filter_by(id=user_id).first()
        if user is not None:

            form = SearchForm()
            block_msg = BlockUserMsg()
            if block_user := BlockUser.query.filter_by(user_id=user_id).first():
                db.session.delete(block_user)
                db.session.commit()
                flash(ADMIN_UNBLOCK_MSG, 'success')
                return redirect(url_for('admin.admin_page'))
            else:
                if block_msg.validate_on_submit():
                    block_user = BlockUser(user_id=user_id, reason=block_msg.reason.data)
                    db.session.add(block_user)
                    db.session.commit()
                    flash(ADMIN_BLOCK_MSG, 'success')
                    return redirect(url_for('admin.admin_page'))
            return render_template('admin_block_user.html', user=user, form=form, block_msg=block_msg)

        else:
            flash(USER_NOT_EXIST_MSG, 'warning')
            return redirect(url_for('admin.admin_page'))
    else:
        flash(admin_access_msg, 'warning')
        return redirect(url_for('main.home_page'))
