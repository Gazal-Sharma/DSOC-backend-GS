from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from data_models import Customer  # Make sure this import is correct
from utils import role_required


customer = Blueprint('customer', __name__, template_folder="templates")

@customer.route('/create', methods = ['POST'])
def create_customer():
    data = request.get_json()
    from app import db, db_connection
    new_customer = Customer(
        c_name=data['c_name'],
        c_email=data['c_email'],
        c_password=data['c_password'],
        c_contact=data['c_contact'],
        c_role=data['c_role'],
        c_status=data.get('c_status', 'active')
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

@customer.route('/get_one/<int:id>', methods=['GET'])
# @login_required
# @role_required('staff', 'admin')
def get_one(id):
    customer = Customer.query.get_or_404(id)
    return jsonify(customer.to_dict()), 200

@customer.route('/get_all', methods = ['GET'])
# @login_required
# @role_required('staff', 'admin')
def get_all():
    customers = Customer.query.all()
    return jsonify([s.to_dict() for s in customers]), 200

@customer.route('/put/<int:id>', methods=['PUT'])
# @login_required
# @role_required('customer')
def update(id):
    data = request.get_json()
    from app import db, db_connection
    customer = Customer.query.get_or_404(id)
    customer.c_name = data['c_name']
    customer.c_email = data['c_email']
    customer.c_password = data['c_password']
    customer.c_role = data['c_role']
    customer.c_contact = data['c_contact']
    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200


@customer.route('/delete/<int:id>', methods = ['DELETE'])
# @login_required
# @role_required('admin')
def delete(id):
    from app import db, db_connection
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})

