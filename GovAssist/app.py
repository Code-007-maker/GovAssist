import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)   # Only define once
app.secret_key = "secret123"

DATABASE = "govassist.db"

# --- Database helper functions ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schemes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                min_age INTEGER,
                max_age INTEGER,
                income_limit INTEGER,
                description TEXT
            )
        ''')
        db.commit()

# --- Routes ---

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if not username or not password:
            return "Please enter username and password"

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return "Username already exists! Please choose another."

        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        db.commit()

        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

        if row and check_password_hash(row["password"], password):
            session["username"] = username
            return redirect(url_for("dashboard"))

        return "Invalid username or password!"

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    schemes = []
    if request.method == "POST":
        age = int(request.form["age"])
        occupation = request.form["occupation"]
        income = int(request.form["income"])
        education = request.form["education"]

        user_data = {
            "age": age,
            "occupation": occupation,
            "income": income,
            "education": education
        }
        all_schemes = [
            {
                "name": "Student Scholarship",
                "criteria": lambda u: u["occupation"] == "student" and u["income"] < 500000,
                "description": "Scholarships for meritorious students with low income."
            },
            {
                "name": "Farmer Subsidy",
                "criteria": lambda u: u["occupation"] == "farmer" and u["income"] < 300000,
                "description": "Subsidies for small-scale farmers."
            },
            {
                "name": "Unemployed Job Training",
                "criteria": lambda u: u["occupation"] == "unemployed" and u["age"] < 35,
                "description": "Job training programs for unemployed youth."
            },
            {
                "name": "Worker Insurance",
                "criteria": lambda u: u["occupation"] == "worker" and u["income"] < 400000,
                "description": "Insurance schemes for workers with low income."
            }
        ]

        schemes = [s for s in all_schemes if s["criteria"](user_data)]

    return render_template("index.html", username=session["username"], schemes=schemes)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("welcome"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
