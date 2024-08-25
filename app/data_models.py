from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import bcrypt
from datetime import datetime

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

    transactions = db.relationship('Transaction', backref='staff', lazy=True, cascade='all, delete-orphan')

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
        
    def to_dict(self):
        return {
            'id': self.s_id,
            'name': self.s_name,
            'email': self.s_email,
            'role': self.s_role,
            'is_approved': self.is_approved
        }
    

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
    
    def to_dict(self):
        return {
            'id': self.c_id,
            'name': self.c_name,
            'email': self.c_email,
            'role': self.c_role,
            'contact': self.c_contact
        }

class Transaction(db.Model):
    __tablename__ = 'transaction'
    t_id = db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, db.ForeignKey('customer.c_id'), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey('staff.s_id'), nullable=False)
    product_amount_list = db.Column(db.JSON, nullable=False)
    t_date = db.Column(db.DateTime, nullable=False,  default=datetime.utcnow)
    t_time = db.Column(db.Time, nullable=False, default=datetime.utcnow().time)
    t_amount = db.Column(db.Numeric(10, 2), nullable=False)
    t_category = db.Column(db.String(50))
    # Relationships
    customer = db.relationship('Customer', backref=db.backref('transactions', lazy=True))
    # staff = db.relationship('Staff', backref=db.backref('transactions', lazy=True))

    def to_dict(self):
        return {
            't_id': self.t_id,
            'c_id': self.c_id,
            's_id': self.s_id,
            'product_amount_list': self.product_amount_list,
            't_date': self.t_date.isoformat(),
            't_time': self.t_time.isoformat(),
            't_amount': self.t_amount,
            't_category': self.t_category
        }