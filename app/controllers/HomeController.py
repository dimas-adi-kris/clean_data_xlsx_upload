
from flask import render_template, request, Blueprint, session,redirect
# from app.models.user import User
import app.models.UserModel as User

from app.middleware.Authentication import authentication
from werkzeug.security import generate_password_hash, check_password_hash


home = Blueprint('home', __name__)

auth = Blueprint('auth', __name__)


@home.route("/", methods=["GET", "POST"])
@home.route('/index', methods=["GET", "POST"])
def index():
    if authentication():
        return render_template("pages/home/index.html")
    else:
        return render_template("pages/auth/login.html")

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/auth/login.html")
    else:
        username = request.form.get("login")
        password = request.form.get("password")
        print(username,password)
        autentikasi = User.check_password(username,password)
        if autentikasi:
            print(autentikasi)
            session["username"] = autentikasi['username']
            session["role"] = autentikasi['role']
            return redirect("/")
        else:
            return render_template("pages/auth/login.html",message="Login failed",status="danger")



@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("pages/auth/register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if User.check_username(username):
            return render_template("pages/auth/register.html",message="Username already exists",status="danger")
        else:
            User.add_user(username,password)
            session["username"] = username
            return render_template("pages/auth/login.html",message="Register success",status="success")
        

@auth.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")