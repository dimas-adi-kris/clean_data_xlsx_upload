from flask import (
    render_template,
    request,
    Blueprint,
    session,
    redirect,
    jsonify,
    flash,
    url_for,
)
import app.models.UserModel as User
import app.models.ActivityModel as Activity
from app.helpers import *


activity = Blueprint("activity", __name__)


@activity.route("/activity", methods=["GET", "POST"])
def view():
    activities = Activity.get_all_data()
    # print(activities)
    return render_template("pages/activity/index.html", activities=activities)


@activity.route("/activity/delete/<id>", methods=["GET", "POST"])
def delete(id):
    Activity.delete_data(id)
    flash("Delete activity success", "success")
    return redirect(url_for("activity.view"))
