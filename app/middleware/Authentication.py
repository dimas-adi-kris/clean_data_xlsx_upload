from flask import session

def authentication():
    if session.get("username") is None:
        return False
    else:
        return True