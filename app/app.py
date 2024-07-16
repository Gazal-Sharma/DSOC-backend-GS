from flask import Flask, render_template, redirect, flash, request, session, url_for, jsonify, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from utils import role_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import psycopg2, pytest
from jinja2 import TemplateNotFound
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

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

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://Admin:icandothis12357@localhost/viewhere'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = "fe69ecb4ba26fe4973b26fb35038c70954d642cadd2a2c0f3828b5325fa27d06"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False  
    app.permanent_session_lifetime = timedelta(minutes = 10)


    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from blueprints.products.get_prod.get_prod import get_ps
    # from blueprints.products.post_prod.post_prod import post_pd
    # from blueprints.products.put_prod.put_prod import put_pd
    # from blueprints.products.delete_prod.delete_prod import delete_ps
    from blueprints.login.login import mains
    from blueprints.users.staff_crud.staff_d import staff_d
    from blueprints.transaction.transaction import trs

    from data_models import Staff
    app.register_blueprint(get_ps)
    # app.register_blueprint(post_pd)
    # app.register_blueprint(put_pd)
    # app.register_blueprint(delete_ps)
    app.register_blueprint(mains)
    app.register_blueprint(staff_d, url_prefix = '/staff_d')
    app.register_blueprint(trs, url_prefix = '/trs')

    return app



db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from data_models import Staff
    return Staff.query.get(int(user_id))










