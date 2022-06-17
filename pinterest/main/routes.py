from flask import Blueprint, render_template
from pinterest.models import Pin
from flask.views import View
from pinterest.main.form import SearchForm

main = Blueprint('main', __name__)


# @main.route("/", methods=['POST', 'GET'])
# def home_page():
#     pins = Pin.query.all()
#     return render_template('home.html', pins=pins)

class HomePage(View):
    def dispatch_request(self):
        pins = Pin.query.all()
        return render_template('home.html', pins=pins)


main.add_url_rule('/', view_func=HomePage.as_view('home_page'))


# for passing the form to the base template
@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    pins = Pin.query.all()
    if form.validate_on_submit():
        searched_pin = form.searched.data
        selected_pins = Pin.query.filter(Pin.title.ilike('%' + searched_pin + '%')).all()
        return render_template('search.html', form=form, selected_pins=selected_pins)
    return render_template('home.html', pins=pins)
