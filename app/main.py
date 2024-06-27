from flask import Flask, render_template, redirect, flash, request, session, url_for
from datetime import timedelta
import psycopg2
import logging


DB_CONFIG = {
    'dbname' : "viewhere",
    'user' : "Admin",
    'password' : "icandothis12357",
    'host' : "localhost",
    'port' : "5432",
}
logging.basicConfig(level=logging.INFO)
def db_connection():
    conn = psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )
    logging.info("Database connection established.")
    yield conn
    return conn

def create_tables():
    conn = db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    with open('sql_script.sql', 'r') as f:
            cur.execute(f.read())
    conn.commit()
    logging.info(f"SQL file executed successfully.")
    cur.close()
    conn.close()
    print("Tables created succesfully")

def insert_data():
    conn = db_connection()
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS InventoryItem')
    insert_data = 'INSERT INTO InventoryItem(Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty) VALUES(%s, %s, %s, %s, %s)'
    insert_value = (1, 'screws', 'twist', 120, 100)
    cur.execute(insert_data, insert_value)
    conn.commit()
    logging.info("Data inserted successfully into InventoryItem.")
    cur.close()
    conn.close()

app = Flask(__name__)
app.secret_key = "DSOC FOR THE WIN" # for flash
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
@app.route('/home')
def home():
    flash("HELLO and WELCOME to the DSOC PROJECT!!!!")
    return render_template("home.html")

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nme"]
        session["user"] = user
        email = request.form["email"]
        session["email"] = email
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

if __name__ == "__main__":
    create_tables()
    insert_data()
    app.run(host='0.0.0.0', debug = True)
