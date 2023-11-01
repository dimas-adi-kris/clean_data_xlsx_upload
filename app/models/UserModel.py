from app.db.mysql_connect import db_mysql, metadata
from sqlalchemy import Table, Column, String, text, insert, select, update, delete
from ordereduuid import OrderedUUID
from werkzeug.security import generate_password_hash, check_password_hash


users = Table(
    "users",
    metadata,
    Column("id", String(255), primary_key=True),
    Column("username", String(255)),
    Column("password", String(255)),
    Column("role", String(255)),
)


def get_all_data():
    data = db_mysql.query(users).all()
    return data


def get_data_by_id(id):
    data = db_mysql.query(users).filter_by(id=id).first()
    if data is None:
        return False
    return data._asdict()


def add_user(username, password, role):
    id = str(OrderedUUID())
    stmt = insert(users).values(
        id=id, username=username, password=generate_password_hash(password), role=role
    )
    db_mysql.execute(stmt)
    return {"id": id, "username": username, "role": role}


def update_data(id, username, password, role):
    stmt = (
        update(users)
        .where(users.c.id == id)
        .values(
            username=username,
            password=generate_password_hash(password),
            role=role,
        )
    )
    db_mysql.execute(stmt)
    return {"id": id, "username": username, "role": role}


def delete_data(id):
    stmt = delete(users).where(users.c.id == id)
    db_mysql.execute(stmt)
    return True


def get_data_by_username(username):
    data = db_mysql.query(users).filter_by(username=username).first()._asdict()
    return data


def check_username(username):
    data = db_mysql.query(users).filter_by(username=username).first()
    if data is None:
        return False
    return data._asdict()


def check_password(username, password):
    data = db_mysql.query(users).filter_by(username=username).first()
    if data is None:
        return False
    data = data._asdict()
    if check_password_hash(data["password"], password):
        return data
    return False


def registerAdmin():
    id = str(OrderedUUID())
    stmt = insert(users).values(
        id=id,
        username="admin",
        password=generate_password_hash("admin"),
        role="admin",
    )
    db_mysql.execute(stmt)
    return {"id": id, "username": "admin"}

def update_password(username, password):
    if check_username(username) == False:
        return False
    stmt = (
        update(users)
        .where(users.c.username == username)
        .values(
            password=generate_password_hash(password),
        )
    )
    res = db_mysql.execute(stmt)
    print(res,stmt)
    return True