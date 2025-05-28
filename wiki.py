from bottle import Bottle, run, template, request, redirect, static_file
import os
import json

app = Bottle()

# Kontrollera att användarkatalogen finns
if not os.path.exists("users"):
    os.makedirs("users")


@app.route("/")
def index():
    return template("index", error="")


@app.route("/signup", method=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.forms.get("username")
        password = request.forms.get("password")
        start_capital = request.forms.get("start_capital")

        if not username or not password or not start_capital:
            return template("signup", error="Alla fält måste fyllas i!")

        if not start_capital.replace(".", "", 1).isdigit():
            return template("signup", error="Startkapitalet måste vara ett nummer!")

        user_file = f"users/{username}.json"
        if os.path.exists(user_file):
            return template("signup", error="Användarnamnet är redan taget!")

        # Spara användaren
        user_data = {"username": username, "password": password, "capital": round(float(start_capital), 2), "trades": []}
        with open(user_file, "w") as f:
            json.dump(user_data, f)

        return redirect("/")

    return template("signup", error="")


@app.route("/guest", method="POST")
def guest_journal():
    username = request.forms.get("username")
    user_file = f"users/{username}.json"

    if not os.path.exists(user_file):
        return template("index", error="Användaren finns inte!")

    with open(user_file, "r") as f:
        user_data = json.load(f)

    return template(
        "journal",
        username=username,
        capital=f"{user_data['capital']:.2f}",
        trades=[{"result": f"{trade['result']:.2f}"} for trade in user_data["trades"]],
        error="",
        guest=True,
    )


@app.route("/login", method="POST")
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    user_file = f"users/{username}.json"

    if not os.path.exists(user_file):
        return template("index", error="Användaren finns inte!")

    with open(user_file, "r") as f:
        user_data = json.load(f)

    if user_data["password"] != password:
        return template("index", error="Fel lösenord!")

    return template(
        "journal",
        username=username,
        capital=f"{user_data['capital']:.2f}",
        trades=[{"result": f"{trade['result']:.2f}"} for trade in user_data["trades"]],
        error="",
        guest=False,
    )


@app.route("/journal/<username>/add", method="POST")
def add_trade(username):
    user_file = f"users/{username}.json"

    if not os.path.exists(user_file):
        return template("index", error="Användaren finns inte!")

    if request.forms.get("guest") == "True":
        return template("journal", username=username, capital="", trades=[], error="Gästanvändare kan inte lägga till trades.", guest=True)

    result = request.forms.get("result")

    try:
        result = round(float(result), 2)
    except ValueError:
        with open(user_file, "r") as f:
            user_data = json.load(f)
        return template(
            "journal",
            username=username,
            capital=f"{user_data['capital']:.2f}",
            trades=[{"result": f"{trade['result']:.2f}"} for trade in user_data["trades"]],
            error="Resultatet måste vara ett nummer!",
            guest=False,
        )

    with open(user_file, "r") as f:
        user_data = json.load(f)

    user_data["capital"] = round(user_data["capital"] + result, 2)
    user_data["trades"].append({"result": result})

    with open(user_file, "w") as f:
        json.dump(user_data, f)

    return template(
        "journal",
        username=username,
        capital=f"{user_data['capital']:.2f}",
        trades=[{"result": f"{trade['result']:.2f}"} for trade in user_data["trades"]],
        error="",
        guest=False,
    )


@app.route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="static")


run(app, host="localhost", port=8080, debug=True)
