from flask import Blueprint, render_template, jsonify, request


delete_ps = Blueprint("delete_pd", __name__, template_folder = "templates")



from flask import Blueprint, render_template, jsonify, request
from app import db_connection

delete_ps = Blueprint("delete_ps", __name__, template_folder="templates")

@delete_ps.route('/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
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
def delete_product_page():
    return render_template('delete_product.html')
