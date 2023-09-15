from app.db.firestore import db
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

    # users_ref = db.collection("users")
    # docs = users_ref.stream()
    # list_users = []
    # for doc in docs:
    #     data = doc.to_dict()
    #     data["id"] = doc.id
    #     del data["password"]
    #     list_users.append(data)
    # return list_users


def get_data_by_id(id):
    data = db_mysql.query(users).filter_by(id=id).first()._asdict()
    return data
    # data = db.collection("users").document(id).get().to_dict()
    # data["id"] = id
    # del data["password"]
    # return data


def add_user(username, password, role):
    id = str(OrderedUUID())
    stmt = insert(users).values(
        id=id, username=username, password=generate_password_hash(password), role=role
    )
    db_mysql.execute(stmt)
    return {"id": id, "username": username, "role": role}
    # id = str(OrderedUUID())
    # doc_ref = db.collection("users").document(id)
    # doc_ref.set(
    #     {
    #         "username": username,
    #         "password": generate_password_hash(password),
    #         "role": role,
    #     }
    # )
    # return {
    #     "id": id,
    #     "username": username,
    # }


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
    # doc_ref = db.collection("users").document(id)
    # doc_ref.set(
    #     {"username": username, "password": generate_password_hash(password), role: role}
    # )
    # return {"id": id, "username": username, "role": role}


def delete_data(id):
    stmt = delete(users).where(users.c.id == id)
    db_mysql.execute(stmt)
    return True
    # db.collection("users").document(id).delete()
    # return True


def get_data_by_username(username):
    data = db_mysql.query(users).filter_by(username=username).first()._asdict()
    return data

    # users_ref = db.collection("users")
    # query = users_ref.where("username", "==", username)
    # docs = query.stream()
    # list_users = []
    # for doc in docs:
    #     data = doc.to_dict()
    #     data["id"] = doc.id
    #     del data["password"]
    #     list_users.append(data)
    # return list_users


def check_username(username):
    data = db_mysql.query(users).filter_by(username=username).first()._asdict()
    return data

    # users_ref = db.collection("users")
    # query = users_ref.where("username", "==", username)
    # docs = query.stream()
    # for doc in docs:
    #     data = doc.to_dict()
    #     return True
    # return False


def check_password(username, password):
    data = db_mysql.query(users).filter_by(username=username).first()._asdict()
    print(data, type(data))
    if check_password_hash(data["password"], password):
        return data
    return False
    # users_ref = db.collection("users")
    # query = users_ref.where("username", "==", username)
    # docs = query.stream()
    # for doc in docs:
    #     data = doc.to_dict()
    #     if check_password_hash(data["password"], password):
    #         data["id"] = doc.id
    #         del data["password"]
    #         return data
    # return False


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
    # id = str(OrderedUUID())
    # doc_ref = db.collection("users").document(id)
    # doc_ref.set(
    #     {
    #         "username": "admin",
    #         "password": generate_password_hash("admin"),
    #         "role": "admin",
    #     }
    # )
    # return {
    #     "id": id,
    #     "username": "admin",
    # }
