from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from data_models import Customer, Transaction
from utils import role_required

trs = Blueprint('trs', __name__, template_folder="templates")

@trs.route('/create', methods=['POST'])
@login_required
def create_trs():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    new_transaction = Transaction(
        c_id=data['c_id'],
        s_id=data['s_id'],
        # product_amount_list=data['product_amount_list'],
        t_date=data['t_date'],
        t_time=data['t_time'],
        t_amount = data['t_amount'],
        t_category = data['t_category']
    )

    existing_transaction = Transaction.query.filter_by(
            c_id=new_transaction.c_id,
            s_id=new_transaction.s_id,
            t_date=new_transaction.t_date,
            t_time=new_transaction.t_time,
            t_amount=new_transaction.t_amount,
            t_category=new_transaction.t_category
        ).first()
    
    if existing_transaction:
        return jsonify({'message': 'transaction already occurred'})
    
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created successfully', 'transaction': new_transaction}), 201

@trs.route('/get_all', methods = ['GET'])
@login_required
def get_trs_all():
    all = Transaction.query.all()
    all_list = [{
        't_id': all.t_id,
        'c_id': all.c_id,
        's_id': all.s_id,
        't_date': all.t_date,
        't_time': all.t_time,
        't_amount': all.t_amount,
        't_category': all.t_category
    } for one in all]
    return jsonify(transactions_list), 200

@trs.route('/get_one/<int:id>', methods = ['GET'])
@login_required
def get_trs_one(id):
    one = Transaction.query.get_or_404(id)

    return jsonify({
        't_id': transaction.t_id,
        'c_id': transaction.c_id,
        's_id': transaction.s_id,
        't_date': transaction.t_date,
        't_time': transaction.t_time,
        't_amount': transaction.t_amount,
        't_category': transaction.t_category
    }), 200

@trs.route('/update/<int:id>', methods = ['PUT'])
@login_required
def update_trs(id):
    trs = Transaction.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    transaction.c_id = data.get('c_id', transaction.c_id)
    transaction.s_id = data.get('s_id', transaction.s_id)
    transaction.t_date = data.get('t_date', transaction.t_date)
    transaction.t_time = data.get('t_time', transaction.t_time)
    transaction.t_amount = data.get('t_amount', transaction.t_amount)
    transaction.t_category = data.get('t_category', transaction.t_category)

    db.session.commit()

    return jsonify({
        'message': 'Transaction updated successfully',
        'transaction_id': transaction.id
    }), 200

@trs.route('/delete/<int:id>', methods = ['DELETE'])
@login_required
def delete_trs(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'}), 204