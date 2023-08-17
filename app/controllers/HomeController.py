
from flask import render_template, request, Blueprint
# from app.models.user import User
from app.models.add_data import add_new_data
from werkzeug.security import generate_password_hash, check_password_hash

home = Blueprint('home', __name__)

auth = Blueprint('auth', __name__)


@home.route("/", methods=["GET", "POST"])
@home.route('/index', methods=["GET", "POST"])
def index():
	return render_template("pages/home/index.html")

@home.route('/add_data', methods=["GET", "POST"])
def add_data():
    add_new_data()
    return render_template("pages/home/index.html")


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/auth/login.html")
    else:
        email = request.form.get("email")

@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("pages/auth/register.html")
    else:
        email = request.form.get("email")