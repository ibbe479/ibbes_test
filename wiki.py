from bottle import Bottle, run, template, request, redirect, static_file
import psycopg2

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="pgserver.mau.se",
            database="test_ibbe",
            user="ao7391",
            password="8hk5hh1b",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Kunde inte ansluta till databasen:", e)
        return None

app = Bottle()

@app.route("/")
def index():
    return template("index", error="")

@app.route("/login", method="POST")
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM log_in WHERE user_name=%s AND lösenord=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return f"<h2>Välkommen, {username}!</h2><a href='/'>Tillbaka</a>"
        else:
            return template("index", error="Fel användarnamn eller lösenord")
    else:
        return template("index", error="Databasfel")

@app.route("/static/<filename>")
def static_files(filename):
    return static_file(filename, root="./static")

run(app, host="localhost", port=8080, debug=True)
