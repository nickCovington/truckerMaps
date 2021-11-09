from enum import unique
import os
import json
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from flask.templating import render_template
from flask_wtf.recaptcha import validators
from werkzeug.utils import redirect
from wtforms.fields.simple import SubmitField
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError

import random
import base64
import requests

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = "testing"

db = SQLAlchemy(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace(
#     "://", "ql://", 1
# )
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    usrType = db.Column(db.String(8))
    email = db.Column(db.String(120))
    fName = db.Column(db.String(120))


class warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address = db.Column(db.String(240), unique=True)


class delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    expectedAt = db.Column(db.String(120))
    deliveredAt = db.Column(db.String(120))
    userID = db.Column(db.Integer, unique=True)
    warehouseID = db.Column(db.Integer, unique=True)
    details = db.Column(db.String(240))


# Registration validation
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("Username already exists, choose a different one")


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


db.create_all()


@app.route("/index")
@login_required
def index():
    return flask.render_template("home.html")


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


@app.route("/invalid")
def invalid():
    return flask.render_template("invalid.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if form.password.data == user.password:
                    login_user(user)
                    return flask.redirect(flask.url_for("home"))
                else:
                    flask.flash("Invalid password")
            else:
                return flask.redirect(flask.url_for("invalid"))

    return flask.render_template("login.html", form=form)


# @app.route("/login", methods=["POST"])
# def login_post():
#     username = flask.request.form.get("username")
#     # query database for the username in the form
#     user = username
#     if user:
#         login_user(user)
#         return flask.redirect(flask.url_for("index"))
#     else:
#         return flask.jsonify({"status": 401, "reason": "Username or Password Error"})


@app.route("/save", methods=["POST"])
def save():
    # add the warehouse location, name, and deliveries.
    return flask.redirect(flask.url_for("home"))


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("home"))
    return flask.redirect(flask.url_for("login"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=False)
