from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import bcrypt

class Staff(db.Model):
    __tablename__ = 'staff'
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(100), unique=True, nullable=False)
    s_email = db.Column(db.String(100), unique=True, nullable=False)
    s_password = db.Column(db.String(128), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    s_role = db.Column(db.String(50), nullable=False)
    s_contact = db.Column(db.String(15))

    # def set_password(self, password):
    #     self.s_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # def check_password(self, password):
    #     return bcrypt.check_password_hash(self.s_password, password)
    
    def is_active(self):
        # Implement logic to determine if the user is active
        return True  # Replace with your actual implementation

    def get_id(self):
        return str(self.s_id)
    def is_authenticated(self):
        return True  # Assuming all staff members are authenticated
    def is_anonymous(self):
        return False

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
class Customer(db.Model, UserMixin):
    __tablename__ = 'customer'

    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(100), unique=True, nullable=False)
    c_email = db.Column(db.String(100), unique=True, nullable=False)
    c_password = db.Column(db.String(128), nullable=False) 
    c_role = db.Column(db.String(50), nullable=False)
    c_contact = db.Column(db.String(15))
    c_status = db.Column(db.String(20), default='active')

    # def set_password(self, password):
    #     self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # def check_password(self, password):
    #     return bcrypt.check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.c_status == 'active'

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('staff.s_id'), nullable=False)
    # product_amount_list = db.Column(db.JSONB, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('transactions', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('transactions', lazy=True))