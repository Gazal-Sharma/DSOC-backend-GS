from flask import Blueprint, jsonify, request, render_template, make_response
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound
from data_models import Customer, Transaction
from utils import role_required
from datetime import datetime, date, time
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
# from weasyprint import HTML
import io
import os
trs = Blueprint('trs', __name__, template_folder="templates")

@trs.route('/create', methods=['POST'])
# @login_required
def create_trs():
    data = request.get_json()
    from data_models import Transaction
    from app import db, db_connection
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    t_date = datetime.strptime(data['t_date'], '%Y-%m-%d') if 't_date' in data else datetime.utcnow().date()
    t_time = datetime.strptime(data['t_time'], '%H:%M:%S').time() if 't_time' in data else datetime.utcnow().time()
    new_transaction = Transaction(
        c_id=data['c_id'],
        s_id=data['s_id'],
        product_amount_list=data['product_amount_list'],
        t_date=t_date,
        t_time=t_time,
        t_amount = data['t_amount'],
        t_category = data['t_category']
    )

    existing_transaction = Transaction.query.filter(
            Transaction.c_id == new_transaction.c_id,
            Transaction.s_id == new_transaction.s_id,
            cast(Transaction.product_amount_list, db.Text) == str(new_transaction.product_amount_list),
            Transaction.t_date==new_transaction.t_date,
            Transaction.t_time==new_transaction.t_time,
            Transaction.t_amount==new_transaction.t_amount,
            Transaction.t_category == new_transaction.t_category
        ).first()
    
    if existing_transaction:
        return jsonify({'message': 'transaction already occurred'})
    
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction created successfully', 'transaction': new_transaction.to_dict()}), 201

@trs.route('/get_all', methods=['GET'])
# @login_required
def get_trs_all():
    transactions = Transaction.query.all()
    transactions_list = [{
        't_id': transaction.t_id,
        'c_id': transaction.c_id,
        's_id': transaction.s_id,
        'product_amount_list': transaction.product_amount_list,
        't_date': transaction.t_date.isoformat(),
        't_time': transaction.t_time.isoformat(),
        't_amount': transaction.t_amount,
        't_category': transaction.t_category
    } for transaction in transactions]
    return jsonify(transactions_list), 200

@trs.route('/get_one/<int:id>', methods=['GET'])
# @login_required
def get_trs_one(id):
    transaction = Transaction.query.get_or_404(id)

    return jsonify({
        't_id': transaction.t_id,
        'c_id': transaction.c_id,
        's_id': transaction.s_id,
        'product_amount_list': transaction.product_amount_list,
        't_date': transaction.t_date.isoformat(),
        't_time': transaction.t_time.isoformat(),
        't_amount': transaction.t_amount,
        't_category': transaction.t_category
    }), 200

@trs.route('/update/<int:id>', methods = ['PUT'])
# @login_required
def update_trs(id):
    transaction = Transaction.query.get_or_404(id)
    data = request.get_json()
    from app import db, db_connection
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    transaction.c_id = data.get('c_id', transaction.c_id)
    transaction.s_id = data.get('s_id', transaction.s_id)
    transaction.product_amount_list = data.get('product_amount_list', transaction.product_amount_list)
    transaction.t_date = data.get('t_date', transaction.t_date)
    transaction.t_time = data.get('t_time', transaction.t_time)
    transaction.t_amount = data.get('t_amount', transaction.t_amount)
    transaction.t_category = data.get('t_category', transaction.t_category)

    db.session.commit()

    return jsonify({
        'message': 'Transaction updated successfully',
        'transaction_id': transaction.t_id
    }), 200

@trs.route('/delete/<int:id>', methods = ['DELETE'])
# @login_required
def delete_trs(id):
    from app import db, db_connection
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'}), 204


@trs.route('/invoice/<int:id>', methods = ['GET'])
def generate_invoice(id):
    transaction = Transaction.query.get_or_404(id)
    rendered = render_template('invoice.html', transaction = transaction)

    pdf = HTML(string = rendered).write_pdf()

    directory = 'store_invoice'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f'store_invoice/invoice_{transaction.t_id}.pdf'
    with open(file_path, 'wb') as f:
        f.write(pdf)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename = invoice_{transaction.t_id}.pdf'

    return response

@trs.route('/invoice/<int:id>/download', methods = ['GET'])
def download_invoice(id):
    file_path = f'store_invoice/invoice_{id}.pdf'

    try:
        with open(file_path, 'rb') as f:
            pdf = f.read()
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=invoice_{id}.pdf'
            return response
    
    except FileNotFoundError:
        return jsonify({'message': 'Invoice not found'}), 404


@trs.route('/transactions/history', methods = ['GET'])
# @login_required
# @role_required('admin')
def transaction_history():
    # if not current_user.is_authenticated:
    #     return jsonify({'message': 'Unauthorized'}), 401

    # Retrieve query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_id = request.args.get('user_id')

    query = Transaction.query

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Transaction.t_date >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Transaction.t_date <= end_date)

    if user_id:
        query = query.filter(Transaction.c_id == user_id)

    transactions = query.all()
    transactions_list = [{
        't_id': transaction.t_id,
        'c_id': transaction.c_id,
        's_id': transaction.s_id,
        'product_amount_list': transaction.product_amount_list,
        't_date': transaction.t_date.isoformat(),
        't_time': transaction.t_time.isoformat(),
        't_amount': transaction.t_amount,
        't_category': transaction.t_category
    } for transaction in transactions]

    return jsonify(transactions_list), 200