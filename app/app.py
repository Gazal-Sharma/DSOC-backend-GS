from flask import Flask, render_template, redirect, flash, request, session, url_for, make_response
from datetime import timedelta
import psycopg2
import pytest

# import connexion

# def create():
#     connexion_app = connexion.App(__name__, specification_dir = '../swagger/')
#     connexion_app.add_api('swagger.yaml')
#     api = connexion_app.app
#     return api

DB_CONFIG = {
    'dbname' : "viewhere",
    'user' : "Admin",
    'password' : "icandothis12357",
    'host' : "localhost",
    'port' : "5432",
}
def db_connection(): 
    conn = psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    return conn

def create_tables():
    conn = db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    with open('sql_script.sql', 'r') as f:
            cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created succesfully")

app = Flask(__name__)
app.secret_key = "DSOC FOR THE WIN" # for flash
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def index():
    # Example of setting Content-Type for HTML response
    response = make_response(render_template('index.html'))
    response.headers['Content-Type'] = 'text/html'
    return response

@app.route('/')
@app.route('/home')
def home():
    flash("HELLO and WELCOME to the DSOC PROJECT!!!!")
    return render_template("home.html")

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        email = request.form["email"]
        session["email"] = email
        contact = request.form["contact"]
        session["contact"] = contact
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO Customer(c_name, c_email, c_contact) VALUES (%s, %s, %s)''',(user, email, contact)
            )
        conn.commit()
        cur.close()
        conn.close()
        flash("Login successful")
        return redirect(url_for("home"))
    else:
        if "user" in session:
            flash("Already Logged in  🤜🤛")
            return redirect(url_for("home"))
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"you have been logged out {user}!!!, come back again ", "info")
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


