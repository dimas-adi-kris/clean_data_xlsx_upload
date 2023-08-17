
from flask import render_template, request, Blueprint, session,redirect
# from app.models.user import User
import app.models.UserModel as User

from app.middleware.Authentication import authentication


admin = Blueprint('admin', __name__)


@admin.route("/admin", methods=["GET", "POST"])
def index():
    if session.get("username") == "admin":
        return render_template("pages/admin/index.html")
    else:
        return render_template("pages/auth/login.html")