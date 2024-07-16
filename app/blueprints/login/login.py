from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils import role_required
from app import bcrypt

mains = Blueprint('mains', __name__, template_folder = "templates",static_folder='static', 
    static_url_path='/login_staff/static/style.css')


@mains.route("/")
@mains.route('/home')
def home():
    flash("HELLO and WELCOME to the DSOC PROJECT!!!!")
    return render_template('home.html')


@mains.route('/login', methods=['GET', 'POST'])
def login():
    from data_models import Staff

    if current_user.is_authenticated:
        flash(f'Already logged in as {current_user.s_name}', 'info')
        return redirect(url_for('mains.home'))

    if request.method == 'POST':
        print(request.form) 
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required')
            return redirect(url_for('mains.login'))

        staff = Staff.query.filter_by(s_email=email).first()
        if staff and bcrypt.check_password_hash(staff.s_password, password):
            if not staff.is_approved:
                flash('Your account is not approved yet.')
                return redirect(url_for('mains.login'))

            login_user(staff)
            flash('Login successful', 'success')
            return redirect(url_for('mains.home'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('mains.login'))

    return render_template('login.html')

@mains.route('/register_staff', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def register_staff():
    from data_models import Staff
    from app import db
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            is_admin = data.get('is_admin', False) 
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            is_admin = 'is_admin' in request.form  
            
        existing_user = Staff.query.filter((Staff.s_email == email) | (Staff.s_name == name)).first()
        if existing_user:
            flash('name or email already exists')
            return render_template('register_staff.html')  

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Determine the role
        role = 'admin' if is_admin else 'staff'

        # Create new staff member
        new_staff = Staff(s_name=name, s_email=email, s_password=hashed_password, s_role=role, is_approved=True)

        # Add to database and commit
        db.session.add(new_staff)
        db.session.commit()

        flash('New staff member registered successfully', 'success')
        return redirect(url_for('mains.home'))

    return render_template('register_staff.html')
 

@mains.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Logged out successfully', 'success')
    else:
        flash('You are not logged in', 'warning')
    return redirect(url_for('mains.home'))

@mains.route("/about")
def about():
    return render_template("about.html")

