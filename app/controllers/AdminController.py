
from flask import render_template, request, Blueprint, session,redirect,jsonify
# from app.models.user import User
import app.models.UserModel as User

from app.middleware.Authentication import authentication


admin = Blueprint('admin', __name__)


@admin.route("/users", methods=["GET", "POST"])
def users():
    if session.get("username") == "admin":
        users = User.get_all_data()
        return render_template("pages/admin/index.html",users=users)
    else:
        return render_template("pages/auth/login.html")
    
@admin.route("/users/store", methods=["GET", "POST"])
def store():
    if session.get("username") == "admin":
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            User.add_user(username,password,role)
            return redirect("/users")
    else:
        return redirect("/login")
    
@admin.route("/users/update/<id>", methods=["GET", "POST"])
def update(id):
    if session.get("username") == "admin":
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            User.update_data(id,username,password,role)
            return redirect("/users")
    else:
        return redirect("/login")
    
@admin.route("/users/delete/<id>", methods=["GET", "POST"])
def delete(id):
    if session.get("username") == "admin":
        User.delete_data(id)
        return redirect("/users")
    else:
        return redirect("/login")

@admin.route("/users/show/<id>", methods=["GET", "POST"])
def show(id):
    if session.get("username") == "admin":
        user = User.get_data_by_id(id)
        return jsonify(user)
    else:
        return redirect("/login")