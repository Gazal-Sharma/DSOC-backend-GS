from flask import Flask, render_template, redirect, flash, request, session, url_for, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import psycopg2, pytest
from jinja2 import TemplateNotFound
from blueprints.get_prod.get_prod import get_p
from blueprints.post_prod.post_prod import post_pd
from blueprints.put_prod.put_prod import put_pd
from blueprints.delete_prod.delete_prod import delete_ps

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
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://Admin:icandothis12357@localhost/viewhere'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "DSOC FOR THE WIN" # for flash
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)

#? ORM SQLALCHEMY
class Products(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float, nullable = False)
    qty = db.Column(db.Integer)

    def __repr__ (self):
        return"<Products(id = '%s', name = '%s', description = '%s', price = '%s', qty = '%s')>" % (
            self.id,
            self.name,
            self.description,
            self.price,
            self.qty
        )

app.register_blueprint(get_p)
app.register_blueprint(post_pd)
app.register_blueprint(put_pd)
app.register_blueprint(delete_ps)

@app.route("/")
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

@app.route('/id')
def get_id():
    return render_template('id.html')


if __name__ == "__main__":
    create_tables()
    app.run(debug = True)


