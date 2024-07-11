from flask import Blueprint, render_template, jsonify, request
from utils import role_required
from flask_login import login_required, current_user



delete_ps = Blueprint("delete_ps", __name__, template_folder="templates")

@delete_ps.route('/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_product(product_id):
    from app import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM InventoryItem WHERE item_SKU = %s', (product_id,))
        conn.commit()
        if cur.rowcount > 0:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@delete_ps.route('/products/delete', methods=['GET'])
@login_required
@role_required('admin')
def delete_product_page():
    return render_template('delete_product.html')
