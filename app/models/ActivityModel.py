from app.db.firestore import db
from ordereduuid import OrderedUUID

def get_all_data():
    activities_ref = db.collection("activities")
    docs = activities_ref.stream()
    list_activities = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        list_activities.append(data)
    return list_activities

def get_data_by_id(id):
    data = db.collection("activities").document(id).get().to_dict()
    data["id"] = id
    return data

def add_activity(name,description):
    id = str(OrderedUUID())
    doc_ref = db.collection("activities").document(id)
    doc_ref.set({"name": name, "description": description})
    return {
        "id":id,
        "name":name,
        "description":description
    }

def update_data(id,name,description):
    doc_ref = db.collection("activities").document(id)
    doc_ref.set({"name": name, "description": description})
    return {
        "id":id,
        "name":name,
        "description":description
    }

def delete_data(id):
    db.collection("activities").document(id).delete()
    return True

def get_data_by_name(name):
    activities_ref = db.collection("activities")
    query = activities_ref.where(u'name', u'==', name)
    docs = query.stream()
    list_activities = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        list_activities.append(data)
    return list_activities
