from flask import session
from functools import wraps
from flask import session, redirect, url_for

def authentication():
    if session.get("username") is None:
        return False
    else:
        return True
    

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if session.get('role') is None:
                return redirect(url_for("auth.login"))
            if session.get("role") not in required_role:
                return redirect(url_for("auth.login"))  # Redirect to login page
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
