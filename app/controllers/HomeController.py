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


def importOnce():
    # Membuat database 'clean_data' jika belum ada
    create_database_query = text(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
    db_mysql.execute(create_database_query)

    # Membuat tabel 'users' jika belum ada
    create_users_table_query = text(
        f"""
        USE {config.DB_NAME};
    CREATE TABLE IF NOT EXISTS {config.DB_NAME}.users (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        role VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

    """
    )
    db_mysql.execute(create_users_table_query)

    # Membuat tabel 'activities' jika belum ada
    create_activities_table_query = text(
        f"""
    CREATE TABLE IF NOT EXISTS {config.DB_NAME}.activities (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        description TEXT
    );

    """
    )
    db_mysql.execute(create_activities_table_query)

    # Commit perubahan ke database
    db_mysql.commit()

    from app.db.firestore import db

    users = Table(
        "users",
        metadata,
        Column("id", String(255), primary_key=True),
        Column("username", String(255), unique=True, nullable=False),
        Column("role", String(255), nullable=False),
        Column("password", String(255), nullable=False),
        extend_existing=True,  # Add this line
    )
    activities = Table(
        "activities",
        metadata,
        Column("id", String(255), primary_key=True),
        Column("username", String(255)),
        Column("description", String(255)),
        extend_existing=True,  # Add this line
    )

    # Check if data exists in the tables before inserting
    if not db_mysql.query(users.select().exists()).scalar():
        users_ref = db.collection("users")
        docs = users_ref.stream()
        data_users = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            del data["password"]
            data_users.append(data)

        for data in data_users:
            id = str(OrderedUUID())  # Make sure OrderedUUID is correctly imported
            username = data["username"]
            password = generate_password_hash("123456")
            role = data["role"]
            stmt = insert(users).values(
                id=id, username=username, role=role, password=password
            )
            db_mysql.execute(stmt)

    if not db_mysql.query(activities.select().exists()).scalar():
        activities_ref = db.collection("activities")
        docs = activities_ref.stream()
        data_activities = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            data_activities.append(data)

        for data in data_activities:
            id = str(OrderedUUID())  # Make sure OrderedUUID is correctly imported
            username = data["username"]
            description = data["description"]
            stmt = insert(activities).values(
                id=id, username=username, description=description
            )
            db_mysql.execute(stmt)

    # Commit the changes
    db_mysql.commit()

    # Close the db_mysql when done
    # db_mysql.close()


@home.route("/", methods=["GET", "POST"])
@home.route("/index", methods=["GET", "POST"])
def index():
    importOnce()
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
        print(username, password)
        autentikasi = User.check_password(username, password)
        if autentikasi:
            print("hello from homecontroller autentikasi")
            print(dict(autentikasi))
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
