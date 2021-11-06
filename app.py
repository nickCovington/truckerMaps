import os
import json
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required

import random
import base64
import requests

app = flask.Flask(__name__)


@app.route("/index")
@login_required
def index():
    return flask.render_template("index.html")


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    # return the user_name from the database and load the user
    return


@app.route("/signup")
def signup():
    return flask.render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = flask.request.form.get("username")
    # check if the user from the form is in the database.
    """""
    if user:
        pass
    else:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    """ ""


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = flask.request.form.get("username")
    # query database for the username in the form
    user = username
    if user:
        login_user(user)
        return flask.redirect(flask.url_for("index"))
    else:
        return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/save", methods=["POST"])
def save():
    # add the warehouse location, name, and deliveries.
    return flask.redirect(flask.url_for("index"))


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("index"))
    return flask.redirect(flask.url_for("login"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=False)
