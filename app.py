import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

def resolve_db_path(value):
    path = Path(value or (BASE_DIR / "lab.db")).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

DB_PATH = resolve_db_path(os.getenv("DB_PATH"))
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
app.secret_key = os.getenv("SECRET_KEY", "local-sqli-lab-change-this-secret")

def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(DB_PATH), timeout=10)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                display_name TEXT NOT NULL
            )
        """)
        count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)",
                [
                    ("analyst", "LabAccess2026!", "Security Analyst"),
                    ("operator", "BlueTeam123!", "Lab Operator"),
                    ("intern", "WelcomeToTheLab!", "Junior Researcher"),
                ],
            )

# Run at import time as well as when started directly. This also supports WSGI imports.
initialize_database()

@app.get("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.post("/login")
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # INTENTIONALLY VULNERABLE: direct interpolation is retained for authorized,
    # local SQL injection training. Never use this pattern in production.
    query = (
        "SELECT id, username, display_name FROM users "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    try:
        with get_db() as db:
            user = db.execute(query).fetchone()
    except sqlite3.Error:
        app.logger.exception("SQLite error during lab login")
        flash("The login query failed. Check the server log for details.", "error")
        return redirect(url_for("index"))

    if user:
        session.clear()
        session["user"] = user["username"]
        session["display_name"] = user["display_name"]
        return redirect(url_for("dashboard"))

    flash("Those credentials didn't match. Try again.", "error")
    return redirect(url_for("index"))

@app.get("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("index"))
    return render_template(
        "index.html",
        authenticated=True,
        display_name=session.get("display_name", session["user"]),
        username=session["user"],
    )

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1").strip()
    port = int(os.getenv("PORT", "5000"))
    if host not in {"127.0.0.1", "localhost"}:
        raise RuntimeError("This intentionally vulnerable lab is restricted to localhost.")
    print(f"[SQLi lab] Database: {DB_PATH}")
    print(f"[SQLi lab] Open http://{host}:{port}")
    app.run(host=host, port=port, debug=False)
