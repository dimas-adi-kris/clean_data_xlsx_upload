from flask import render_template, request, Blueprint, session,redirect,jsonify,flash
import app.models.UserModel as User
import app.models.ActivityModel as Activity
from app.helpers import *


activity = Blueprint('activity', __name__)


@activity.route("/activity", methods=["GET", "POST"])
def activity():
    activities = Activity.get_all_data()
    return render_template("pages/activity/index.html",activities=activities)