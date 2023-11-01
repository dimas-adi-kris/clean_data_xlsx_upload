from flask import render_template, request, Blueprint, session, redirect, flash
from app.db.mysql_connect import db_mysql, metadata
from sqlalchemy import Table, Column, String, text, insert, select
from ordereduuid import OrderedUUID
from app.models import UserModel, ActivityModel
import config

# from app.db.mysql_connect import ExecuteOnce

# from app.models.user import User
import app.models.UserModel as User

from app.middleware.Authentication import authentication
from werkzeug.security import generate_password_hash, check_password_hash


home = Blueprint("home", __name__)

auth = Blueprint("auth", __name__)

@home.route("/", methods=["GET", "POST"])
@home.route("/index", methods=["GET", "POST"])
def index():
    if authentication():
        return render_template("pages/home/index.html")
    else:
        return render_template("pages/auth/login.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/auth/login.html")
    else:
        username = request.form.get("login")
        password = request.form.get("password")
        autentikasi = User.check_password(username, password)
        if autentikasi:
            session["username"] = autentikasi["username"]
            session["role"] = autentikasi["role"]
            return redirect("/")
        else:
            flash("Katasandi salah", "danger")
            return render_template(
                "pages/auth/login.html", message="Login failed", status="danger"
            )


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("pages/auth/register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if User.check_username(username):
            return render_template(
                "pages/auth/register.html",
                message="Username already exists",
                status="danger",
            )
        else:
            User.add_user(username, password)
            session["username"] = username
            return render_template(
                "pages/auth/login.html", message="Register success", status="success"
            )


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/")

@auth.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "GET":
        return render_template("pages/auth/forget-password.html")
    else:
        username = request.form.get("login")
        password = '123456'
        if User.update_password(username, password):
            flash("Reset password success", "success")
        else:
            flash("Usename tidak ditemukan", "danger")
        return redirect("/login")