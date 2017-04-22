import requests
from flask import Flask, request, Response, render_template
from functools import wraps

app = Flask(__name__)



def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # This is bad: fix if actually going to use on a larger scale:
    return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# examples
@app.route('/')
@requires_auth
def welcome():
    return "This works" # render_template('set_layout.html')

@app.route('/secret-page')
@requires_auth
def secret_page():
    return "YOu are doomed!"

if __name__ == "__main__":
    app.run()