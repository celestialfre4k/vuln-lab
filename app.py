import os
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect
)


# =========================================
# Flask App Configuration
# =========================================

app = Flask(__name__)

app.secret_key = "supersecretkey"


# =========================================
# Project Paths
# =========================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "database" / "users.db"

VULNERABLE_FILES_DIR = BASE_DIR / "vulnerable_files"


# =========================================
# Home Route
# =========================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================
# XSS Lab
# =========================================

@app.route("/xss")
def xss():

    name = request.args.get("name", "")

    output = f"Hello {name}"

    return render_template(
        "xss.html",
        output=output
    )


# =========================================
# SQL Injection Lab
# =========================================

@app.route("/sqli")
def sqli():

    username = request.args.get("username", "")

    conn = sqlite3.connect(str(DATABASE_PATH))

    cursor = conn.cursor()

    # INTENTIONALLY VULNERABLE
    query = f"""
    SELECT * FROM users
    WHERE username = '{username}'
    """

    try:

        results = cursor.execute(query).fetchall()

        output = results

    except Exception as e:

        output = str(e)

    conn.close()

    return render_template(
        "sqli.html",
        output=output
    )


# =========================================
# Authentication Bypass Lab
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = sqlite3.connect(str(DATABASE_PATH))

        cursor = conn.cursor()

        # INTENTIONALLY VULNERABLE
        query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        """

        print(query)

        result = cursor.execute(query).fetchone()

        print(result)

        conn.close()

        if result:

            session["user"] = username

            return redirect("/dashboard")

        else:

            message = "Invalid credentials"

    return render_template(
        "login.html",
        message=message
    )


# =========================================
# Dashboard Route
# =========================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")

    return f"""
    <h1>Welcome {session["user"]}</h1>

    <p>
        You are logged into VulnLab.
    </p>
    """


# =========================================
# Logout Route
# =========================================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


# =========================================
# Command Injection Lab
# =========================================

@app.route("/command")
def command():

    ip = request.args.get("ip", "")

    output = ""

    if ip:

        command = f"ping {ip}"

        output = os.popen(command).read()

    return render_template(
        "command.html",
        output=output
    )


# =========================================
# Path Traversal Lab
# =========================================

@app.route("/traversal")
def traversal():

    filename = request.args.get("file", "")

    output = ""

    if filename:

        # Convert the vulnerable directory into an absolute path
        base_directory = VULNERABLE_FILES_DIR.resolve()

        # Combine the user supplied filename with the vulnerable directory
        requested_file = (base_directory / filename).resolve()

        try:

            # INTENTIONALLY VULNERABLE
            #
            # We deliberately DO NOT check whether requested_file
            # stays inside base_directory.
            #
            # This allows ../ traversal for this educational lab.

            with open(
                requested_file,
                "r",
                encoding="utf-8"
            ) as file:

                output = file.read()

        except Exception as e:

            output = str(e)

    return render_template(
        "traversal.html",
        output=output
    )


# =========================================
# Run Flask Application
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=8080
    )