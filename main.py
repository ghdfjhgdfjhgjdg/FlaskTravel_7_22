from flask import Flask, render_template, request, abort, make_response, redirect, url_for
import os
import data
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",
                           departures=data.departures,
                           title = data.title,
                           subtitle=data.subtitle,
                           description=data.description,
                           tours=data.tours,
                           cookie=request.cookies.get("username"))

@app.route("/departures/")
def departures():
    return render_template("index.html")

@app.route("/departures/<departure>/")
def departure(departure):
    tours = dict(filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    if tours:
        return render_template("departure.html",
                               departure=departure,
                               title=data.title,
                               departures=data.departures,
                               tours=tours)
    abort(404)


@app.route("/tours/")
def list_tours():
    return render_template("tour.html")

@app.route("/tours/<int:id>/")
def tours(id):
    return render_template("tour.html",
                           tour=data.tours[id],
                           title=data.title,
                           departures=data.departures)

@app.route("/login/", methods=["GET", "POST"])
def login():
    if not request.cookies.get("username") and request.method == "POST":
        res = make_response("Setting a cookie")
        res.set_cookie("username", request.form.get("name"), max_age=60 * 60 * 24 * 365 * 2)
        return res
    return render_template("login.html")

@app.route("/cookie/")
def cookie():
    if not request.cookies.get("username") or request.cookies.get("username") == "None":
        return redirect(url_for("login"))
    else:
        res = make_response(f"Value of cookies is {request.cookies.get('username')}")
        return res


@app.route("/agent/")
def agent():
    user_agent = request.headers.get("User-Agent")
    return f"<b>Your browser is {user_agent}</b>"



app.run(port=35000, debug=True)
