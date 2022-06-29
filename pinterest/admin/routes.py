from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from pinterest.main.form import SearchForm
from flask_login import current_user, login_required
from pinterest.models import Tags
from pinterest import db
from pinterest.admin.form import UpdateTagForm

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
        return render_template('admin.html', tags=tags, form=form)
    else:
        flash('You dont have access to this page', 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/tags/new", methods=['POST', 'GET'])
@login_required
def admin_new_tag():

    """create new pin.
    :return: admin home page
    """

    id = current_user.id
    if id == 1:
        form = UpdateTagForm()
        if form.validate_on_submit():
            new_tag = Tags(name=form.name.data)
            db.session.add(new_tag)
            db.session.commit()
            flash('Tag has been created', 'success')
            return redirect(url_for('admin.admin_page'))
        return render_template('admin_new_tag.html', form=form)
    else:
        flash('You dont have access to this page', 'warning')
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
                flash('Tag has been updated', 'success')
                return redirect(url_for('admin.admin_page'))
            return render_template('admin_update_tag.html', form=form, tag=tag)
        else:
            flash('Tag does not exist...!!!', 'warning')
            return redirect(url_for('admin.admin_page'))
    else:
        flash('You dont have access to this page', 'warning')
        return redirect(url_for('main.home_page'))


@admin.route("/admin/tags/<int:tag_id>/delete", methods=['POST', 'GET'])
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
            flash('Tag has been deleted...!!!', 'success')
            return redirect(url_for('admin.admin_page'))
        else:
            flash('Tag does not exist', 'warning')
            return redirect(url_for('admin.admin_page'))
    else:
        flash('You dont have access to this page', 'warning')
        return redirect(url_for('main.home_page'))
