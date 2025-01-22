from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "98123"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///koobi.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    welcome = db.execute("SELECT username FROM users WHERE id = ?", user_id)

    db.execute("DELETE FROM notes WHERE rowid NOT IN (SELECT MIN(rowid) FROM notes GROUP BY title, note, date)")

    notes = db.execute("SELECT id, title, note, date FROM notes WHERE user_id = ? ORDER BY date DESC", user_id)

    return render_template("notes.html", welcome=welcome[0]['username'], notes=notes)


@app.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            print("oi")
            flash("Must provide username", "error")
            return redirect("/login")

        elif not password:
            flash("Must provide password", "error")
            return redirect("/login")

        users = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
            flash("Invalid username and/or password", "error")
            return redirect("/login")
        
        session.clear()

        session["user_id"] = users[0]["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("newusername")
        password = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        usernames = [user['username'] for user in db.execute("SELECT username FROM users")]

        lenpassword = len(password)

        if not username:
            flash("Must provide username.", "error")
            return redirect("/register")
        elif username in usernames:
            flash("Username already exists.", "error")
            return redirect("/register")
        elif not password:
            flash("Must provide password.", "error")
            return redirect("/register")
        elif lenpassword > 8:
            flash("Password must have a maximum of 8 characters.", "error")
            return redirect("/register")
        elif lenpassword < 4:
            flash("Password must have a minimum of 4 characters.", "error")
            return redirect("/register")
        elif not confirmation:
            flash("Must provide confirmation.", "error")
            return redirect("/register")
        elif password != confirmation:
            flash("Passwords don't match.")
            return redirect("/register")
        else:
            hash = generate_password_hash(password)

            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            
            flash("Registration Succesful.", "message")
            return redirect("/login")
    else:
        return render_template("register.html")
    

@app.route("/newnote", methods = ["GET", "POST"])
@login_required
def newnote():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        user_id = session['user_id']
        time = datetime.datetime.now()

        db.execute("INSERT INTO notes (user_id, title, note, date) VALUES (?, ?, ?, ?)", user_id, title, text, time)

        return redirect("/")

    else:
        user_id = session["user_id"]
        welcome = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        return render_template("newnote.html", welcome=welcome[0]["username"])


@app.route("/edit/<int:nota_id>", methods = ["GET", "POST"])
@login_required
def edit(nota_id):
    user_id = session['user_id']

    if request.method == "POST":
        title = request.form.get("titleedit")
        note = request.form.get("textedit")
        date = datetime.datetime.now()

        db.execute("UPDATE notes SET title = ?, note = ?, date = ? WHERE user_id = ? AND id = ?", title, note, date, user_id, nota_id)

        flash("Edit Succesful.", "message")
        return redirect("/")

    else:
        nota = db.execute("SELECT title, note, date, id FROM notes WHERE id = ?", nota_id)
        welcome = db.execute("SELECT username FROM users WHERE id = ?", user_id)

        return render_template("edit.html", welcome=welcome[0]["username"], notes=nota)


@app.route("/delete/<int:nota_id>")
def delete(nota_id):
    user_id = session['user_id']
    db.execute("DELETE FROM notes WHERE user_id = ? AND id = ?", user_id, nota_id)
    return redirect("/")