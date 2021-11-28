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
from wtforms import RadioField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from places_api import PLACES_API_KEY, getPlaceInfo

import random
import base64
import requests

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = "testing"

db = SQLAlchemy(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL").replace(
#     "://", "ql://", 1
#)
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
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    name = db.Column(db.String(120))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address = db.Column(db.String(240))


class delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.String(120))
    endDate = db.Column(db.String(120))
    expectedAt = db.Column(db.String(120))
    deliveredAt = db.Column(db.String(120))
    userID = db.Column(db.Integer)
    warehouseID = db.Column(db.Integer)
    details = db.Column(db.String(240))


# Registration validation
class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Username"},
    )
    usrType = StringField(
        validators=[InputRequired(), Length(min=7, max=8)],
        render_kw={"placeholder": "User Type - Manager or Trucker"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=2, max=63)],
        render_kw={"placeholder": "Password"},
    )
    boolchoice = RadioField(
        "Label", choices=[("manager", "Manager"), ("trucker", "Trucker")]
    )

    submit = SubmitField("SignUp")

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


class UpdateForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=0, max=63)],
        render_kw={"placeholder": "Username"},
    )
    usrType = StringField(
        validators=[InputRequired(), Length(min=0, max=8)],
        render_kw={"placeholder": "Change user type - Manager or Trucker"},
    )
    email = StringField(
        validators=[InputRequired(), Length(min=0, max=63)],
        render_kw={"placeholder": "Enter new email"},
    )
    fName = StringField(
        validators=[InputRequired(), Length(min=0, max=63)],
        render_kw={"placeholder": "Update your full name"},
    )

    submit = SubmitField("Update Profile")


db.create_all()


def get_profile_details():
    id = flask_login.current_user.id
    usrType = flask_login.current_user.usrType
    userName = flask_login.current_user.username
    try:
        email = flask_login.current_user.email
        fName = flask_login.current_user.fName
    except:
        email = "No email given"
        fName = flask_login.current_user.fName
    profile_details = {
        "id": id,
        "usrType": usrType,
        "userName": userName,
        "email": email,
        "fName": fName,
    }
    return profile_details


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    userID = flask_login.current_user.id

    googleMapURL = None

    # if user attempts to add new location
    if flask.request.method == "POST":
        locationToAdd = flask.request.form.get("location-to-add")

        # url to dynamically generate a google map based on user-input
        googleMapURL = (
            "https://www.google.com/maps/embed/v1/place?key="
            + PLACES_API_KEY
            + "&q="
            + locationToAdd
        )

        # placeInfo = dictionary containing {address, lat, lon, name}
        placeInfo = getPlaceInfo(locationToAdd)

        address = placeInfo["address"]
        latitude = placeInfo["lat"]
        longitude = placeInfo["lon"]
        name = placeInfo["name"]

        wexists = warehouse.query.filter_by(address=address, userID=userID).first()
        if wexists:
            flask.flash(address + " already exists in your saved list")
        else:
            new_w = warehouse(
                name=name, address=address, lat=latitude, lng=longitude, userID=userID
            )
            db.session.add(new_w)
            db.session.commit()

            flask.flash(placeInfo["address"] + " has been successfully added.")

    w_list = warehouse.query.filter_by(userID=userID).all()
    existing_adds = []
    add_ids = []
    for wh in w_list:
        existing_adds.append(wh.address)
        add_ids.append(wh.id)
    
    print(f"before d_list id={userID}")
    d_list = delivery.query.filter_by(userID=userID).all()
    existing_dels = []
    del_ids = []
    for de in d_list:
        existing_dels.append([de.warehouseID, de.startDate, de.expectedAt])
        del_ids.append(de.id)

    try:
        dlen = len(existing_dels)
    except:
        dlen = 0
    
    return flask.render_template(
        "home.html", 
        usern=flask_login.current_user.username,
        warehouses=existing_adds,
        len=len(existing_adds),
        len2=dlen,
        deliveries=existing_dels,
        googleMapURL=googleMapURL,
        del_ids=del_ids,
        wh_ids=add_ids
    )

@app.route("/add_delivery", methods=["GET", "POST"])
@login_required
def add_delivery():
    userID = flask_login.current_user.id
    googleMapURL = None

    if flask.request.method == "POST":
        startDate = flask.request.form.get("start")
        expectedAt = flask.request.form.get("expected")
        details = flask.request.form.get("note")
        googleMapURL = (
            "https://www.google.com/maps/embed/v1/place?key="
            + PLACES_API_KEY
            + "&q="
            + flask.request.form.get("address")
        )
        placeInfo = getPlaceInfo(flask.request.form.get("address"))
        wAdd = placeInfo["address"]
        wexists = warehouse.query.filter_by(address=wAdd, userID=userID).first()
        if not wexists:
            new_w = warehouse(
                name=placeInfo["name"], address=wAdd, lat=placeInfo["lat"], lng=placeInfo["lon"], userID=userID
            )
            db.session.add(new_w)
            db.session.commit()
        wID = warehouse.query.filter_by(address=wAdd, userID=userID).first().id

        dexists = delivery.query.filter_by(userID=userID, expectedAt=expectedAt, warehouseID=wID).first()
        if dexists:
            print("not new")
            flask.flash("This exact delivery already exists")
        else:
            print("new delivery")
            new_d = delivery(
                startDate=startDate, expectedAt=expectedAt, userID=userID, warehouseID=wID, details=details   
            )
            db.session.add(new_d)
            db.session.commit()

    w_list = warehouse.query.filter_by(userID=userID).all()
    existing_adds = []
    add_ids = []
    for wh in w_list:
        existing_adds.append(wh.address)
        add_ids.append(wh.id)
    
    print(f"before d_list id={userID}")
    d_list = delivery.query.filter_by(userID=userID).all()
    existing_dels = []
    del_ids = []
    for de in d_list:
        existing_dels.append([de.warehouseID, de.startDate, de.expectedAt])
        del_ids.append(de.id)

    try:
        dlen = len(existing_dels)
    except:
        dlen = 0
    
    return flask.render_template(
        "home.html", 
        usern=flask_login.current_user.username,
        warehouses=existing_adds,
        len=len(existing_adds),
        len2=dlen,
        deliveries=existing_dels,
        googleMapURL=googleMapURL,
        del_ids=del_ids,
        wh_ids=add_ids
    )


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    return flask.render_template("profile.html", data=get_profile_details())


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = UpdateForm()
    if flask.request.method == "POST":
        if form.validate_on_submit():
            curr = User.query.filter_by(
                username=flask_login.current_user.username
            ).first()
            if form.fName.data != None:
                curr.fName = form.fName.data
            if form.username.data != None:
                curr.usernme = form.username.data
            if form.email.data != None:
                curr.email = form.email.data
            if form.usrType.data != None:
                curr.usrType = form.usrType.data
            db.session.commit()
            return flask.redirect(flask.url_for("profile"))
    return flask.render_template("edit.html", form=form, data=get_profile_details())


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    # check if the user from the form is in the database.
    form = RegisterForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            new_user = User(
                username=form.username.data,
                usrType=form.usrType.data,
                password=form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()
            return flask.redirect(flask.url_for("login"))
        else:
            flask.flash("Username already exists")

    return flask.render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
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


@app.route("/invalid")
def invalid():
    return flask.render_template("invalid.html")


@app.route("/save", methods=["POST"])
def save():
    # add the warehouse location, name, and deliveries.
    return flask.redirect(flask.url_for("home"))


@app.route("/")
def main():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("home"))
    return flask.redirect(flask.url_for("login"))

@app.route('/deleteD/<int:id>')
def deleteD(id):
    del_to_delete = delivery.query.get_or_404(id)

    try:
        db.session.delete(del_to_delete)
        db.session.commit()
        flask.flash("Delivery deleted successfully")
        return flask.redirect(flask.url_for("home"))
    except:
        flask.flash("Unable to delete delivery")
        return flask.redirect(flask.url_for("home"))

@app.route('/deleteW/<int:id>')
def deleteW(id):
    del_to_delete = warehouse.query.get_or_404(id)

    try:
        db.session.delete(del_to_delete)
        db.session.commit()
        flask.flash("Warehouse deleted successfully")
        return flask.redirect(flask.url_for("home"))
    except:
        flask.flash("Unable to delete warehouse")
        return flask.redirect(flask.url_for("home"))

app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=False)
