from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from data_models import Staff  # Make sure this import is correct
from utils import role_required


staff_d = Blueprint('staff_d', __name__, template_folder="templates")  # prefix = staff_d

@staff_d.route('/create_staff', methods=['POST']) ## change this to authentication after frontend
# @login_required
# @role_required('admin')
def create_staff():
    # if not current_user.is_admin:
    #     return jsonify({'message': 'Admin access required'}), 403
    from app import db, db_connection
    data = request.get_json()
    new_staff = Staff(
        s_name=data['s_name'],
        s_email=data['s_email'],
        s_password=data['s_password'],
        s_role=data['s_role'],
        s_contact=data['s_contact'],
        is_approved=False
    )
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({'message': 'Staff created successfully'}), 201

@staff_d.route('/get_all', methods=['GET'])
# @login_required
# @role_required('admin', 'staff')
def get_all():
    # if not current_user.is_admin:
    #     return jsonify({'message': 'Admin access required'}), 403
    
    staff_list = Staff.query.all()
    return jsonify([s.to_dict() for s in staff_list]), 200

@staff_d.route('/get_one/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'staff')
def get_one(id):
    staff = Staff.query.get_or_404(id)
    return jsonify(staff.to_dict()), 200

@staff_d.route('/put/<int:id>', methods=['PUT'])
# @login_required
# @role_required('admin')
def put_staff(id):
    from app import db, db_connection
    data = request.get_json()
    staff = Staff.query.get_or_404(id)
    staff.s_name = data['s_name']
    staff.s_email = data['s_email']
    staff.s_role = data['s_role']
    staff.s_contact = data['s_contact']
    db.session.commit()
    return jsonify({'message': 'Staff updated successfully'}), 200

@staff_d.route('/delete_staff/<int:id>', methods=['DELETE'])
# @login_required
# @role_required('admin')
def delete_staff(id):
    from app import db, db_connection
    staff = Staff.query.get_or_404(id)
    db.session.delete(staff)
    db.session.commit()
    return jsonify({'message': 'Staff deleted successfully'}), 200

@staff_d.route('/approve_staff/<int:id>', methods=['PUT'])
@login_required
@role_required('admin')
def approve_staff(id):
    staff = Staff.query.get_or_404(id)
    staff.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Staff approved successfully'}), 200