
from flask import render_template, request, Blueprint, session,redirect,jsonify,flash
# from app.models.user import User
import app.models.UserModel as User
from app.helpers import *

from app.middleware.Authentication import authentication, role_required


admin = Blueprint('admin', __name__)


@admin.route("/users", methods=["GET", "POST"])
@role_required(required_role="admin")
def users():
    users = User.get_all_data()
    return render_template("pages/admin/index.html",users=users)
    
@admin.route("/users/store", methods=["GET", "POST"])
@role_required(required_role="admin")
def store():
    if request.method == "POST":
        username = request.form["username"]
        if User.check_username(username):
            flash("Username sudah ada","danger")
            return redirect("/users")
        if is_valid_username(username) == False:
            flash("Username hanya boleh berisi huruf (baik besar maupun kecil), angka, dan underscore. Panjang username minimal 3 karakter dan maksimal 20 karakter","danger")
            return redirect("/users")
        password = request.form["password"]
        role = request.form["role"]
        User.add_user(username,password,role)
        flash("User berhasil ditambah","success")
        return redirect("/users")
    
@admin.route("/users/update/<id>", methods=["GET", "POST"])
@role_required(required_role="admin")
def update(id):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        User.update_data(id,username,password,role)
        return redirect("/users")
    
@admin.route("/users/delete/<id>", methods=["GET", "POST"])
@role_required(required_role="admin")
def delete(id):
    User.delete_data(id)
    flash("User berhasil dihapus","success")
    return redirect("/users")

@admin.route("/users/show/<id>", methods=["GET", "POST"])
@role_required(required_role="admin")
def show(id):
    user = User.get_data_by_id(id)
    return jsonify(user)