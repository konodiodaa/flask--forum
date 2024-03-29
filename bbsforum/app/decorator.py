from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps


# login limitation decorator
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
