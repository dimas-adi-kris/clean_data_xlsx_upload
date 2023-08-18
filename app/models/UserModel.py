from app.db.firestore import db
from ordereduuid import OrderedUUID
from werkzeug.security import generate_password_hash, check_password_hash

def get_data_by_id(id):
    data = db.collection("users").document(id).get().to_dict()
    data["id"] = id
    del data["password"]
    return data

def add_user(username,password,role):
    id = str(OrderedUUID())
    doc_ref = db.collection("users").document(id)
    doc_ref.set({"username": username, "password": generate_password_hash(password), "role": role})
    return {
        "id":id,
        "username":username,
    }

def update_data(id,username,password,role):
    doc_ref = db.collection("users").document(id)
    doc_ref.set({"username": username, "password": generate_password_hash(password),role:role})
    return {
        "id":id,
        "username":username,
        "role":role
    }

def delete_data(id):
    db.collection("users").document(id).delete()
    return True

def get_all_data():
    users_ref = db.collection("users")
    docs = users_ref.stream()
    list_users = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        del data["password"]
        list_users.append(data)
    return list_users

def get_data_by_username(username):
    users_ref = db.collection("users")
    query = users_ref.where(u'username', u'==', username)
    docs = query.stream()
    list_users = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        del data["password"]
        list_users.append(data)
    return list_users

def check_username(username):
    users_ref = db.collection("users")
    query = users_ref.where(u'username', u'==', username)
    docs = query.stream()
    for doc in docs:
        data = doc.to_dict()
        return True
    return False

def check_password(username,password):
    users_ref = db.collection("users")
    query = users_ref.where(u'username', u'==', username)
    docs = query.stream()
    for doc in docs:
        data = doc.to_dict()
        if check_password_hash(data["password"],password):
            data["id"] = doc.id
            del data["password"]
            return data
    return False