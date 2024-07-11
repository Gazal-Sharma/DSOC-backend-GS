from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from utils import role_required
from flask_login import login_required, current_user

get_ps = Blueprint("get_ps", __name__, template_folder = "templates")

#### get all products


@get_ps.route('/products', methods = ['GET'])
@login_required
@role_required('staff','admin')
def get_products():
    from app import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM InventoryItem')
    products = cur.fetchall()
    conn.close()
    return render_template('get_all.html', products = products)
    # return jsonify(products)



@get_ps.route('/products/<int:product_id>', methods = ['GET','POST'])
@login_required
@role_required('staff','admin')
def get_product(product_id):
    if request.method == "POST":
        product_id = request.form["product_id"]
        return redirect(url_for('get_ps.get_product', product_id=product_id))
    from app import db, db_connection
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM InventoryItem WHERE item_SKU = %s', (product_id,))
    product = cur.fetchone()
    conn.close()
    if product:
        return render_template('get_one.html', product=product)
    else:
        return jsonify({'error': 'Product not found'}), 404