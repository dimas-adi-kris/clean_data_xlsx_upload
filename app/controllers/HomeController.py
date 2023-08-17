
from flask import render_template, Blueprint
# from app.models.user import User
from app.models.add_data import add_new_data

home = Blueprint('home', __name__)


@home.route("/", methods=["GET", "POST"])
@home.route('/index', methods=["GET", "POST"])
def index():
	return render_template("pages/home/index.html")

@home.route('/add_data', methods=["GET", "POST"])
def add_data():
    add_new_data()
    return render_template("pages/home/index.html")