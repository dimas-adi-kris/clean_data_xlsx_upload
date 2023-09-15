from app.db.firestore import db
from app.db.mysql_connect import db_mysql, metadata
from sqlalchemy import Table, Column, String, text, insert, select, update, delete
from ordereduuid import OrderedUUID


activity = Table(
    "activities",
    metadata,
    Column("id", String(255), primary_key=True),
    Column("username", String(255)),
    Column("description", String(255)),
)


def get_all_data():
    activities = db_mysql.query(activity).all()
    return activities


def get_data_by_id(id):
    activities = db_mysql.query(activity).filter_by(id=id).first()._asdict()
    return activities
    # data = db.collection("activities").document(id).get().to_dict()
    # data["id"] = id
    # return data


def add_activity(username, description):
    id = str(OrderedUUID())
    stmt = insert(activity).values(id=id, username=username, description=description)
    db_mysql.execute(stmt)
    return {"id": id, "username": username, "description": description}

    # id = str(OrderedUUID())
    # doc_ref = db.collection("activities").document(id)
    # doc_ref.set({"username": username, "description": description})
    # return {"id": id, "username": username, "description": description}


def update_data(id, name, description):
    stmt = (
        update(activity)
        .where(activity.c.id == id)
        .values(username=name, description=description)
    )
    db_mysql.execute(stmt)
    return {"id": id, "username": name, "description": description}

    # doc_ref = db.collection("activities").document(id)
    # doc_ref.set({"username": name, "description": description})
    # return {"id": id, "username": name, "description": description}


def delete_data(id):
    stmt = delete(activity).where(activity.c.id == id)
    db_mysql.execute(stmt)
    return True
    # db.collection("activities").document(id).delete()
    # return True


def get_data_by_name(name):
    activities = db_mysql.query(activity).filter_by(username=name).all()
    return activities
    # activities_ref = db.collection("activities")
    # query = activities_ref.where("name", "==", name)
    # docs = query.stream()
    # list_activities = []
    # for doc in docs:
    #     data = doc.to_dict()
    #     data["id"] = doc.id
    #     list_activities.append(data)
    # return list_activities
