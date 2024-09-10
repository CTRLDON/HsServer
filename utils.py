from flask import redirect, url_for, session
from functools import wraps


def login_status(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        # Check if user is logged in
        if 'username' not in session.keys():
            # print(session['username'])
            return redirect('/home') # User is not logged in; redirect to login page
        
        return func(*args, **kwargs)
    
    return decorator


def set_session(username: str, email: str, remember_me: bool = False) -> None:
    session['username'] = username
    session['email'] = email
    session.permanent = remember_me