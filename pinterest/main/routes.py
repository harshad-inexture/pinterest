from flask import Blueprint
from flask import render_template
from pinterest.models import Pin

main = Blueprint('main',__name__)

@main.route("/", methods=['POST', 'GET'])
def home_page():
    pins = Pin.query.all()
    return render_template('home.html', pins=pins)