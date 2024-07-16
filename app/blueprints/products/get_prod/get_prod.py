from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from utils import role_required
from flask_login import login_required, current_user

get_ps = Blueprint("get_ps", __name__, template_folder = "templates")


@get_ps.route('/p-home')
def phome():
    # flash("HELLO and WELCOME to the DSOC PROJECT!!!!")
    return render_template('get.html')


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

@get_ps.route('/create/product', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_product():
    if request.method == "POST":
        ITEM_SKU = request.form["ITEM_SKU"]
        ITEM_NAME = request.form["ITEM_NAME"] 
        ITEM_DESCRIPTION = request.form["ITEM_DESCRIPTION"]
        ITEM_PRICE = request.form["ITEM_PRICE"]
        ITEM_QTY = request.form["ITEM_QTY"]
        
        if not all([ITEM_SKU, ITEM_NAME, ITEM_DESCRIPTION, ITEM_PRICE, ITEM_QTY]):
            return jsonify({'error': 'Missing form data'}), 400

        product = {
            "Item_SKU": ITEM_SKU,
            "Item_Name": ITEM_NAME,
            "Item_Description": ITEM_DESCRIPTION,
            "Item_Price": ITEM_PRICE,
            "Item_Qty": ITEM_QTY
        }

        # Assuming db_connection and db are imported correctly
        from app import db, db_connection
        conn = db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                '''INSERT INTO InventoryItem (Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty)
                   VALUES (%s, %s, %s, %s, %s)''',
                (ITEM_SKU, ITEM_NAME, ITEM_DESCRIPTION, ITEM_PRICE, ITEM_QTY)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify({'error': 'Database error: ' + str(e)}), 500
        finally:
            cur.close()
            conn.close()
        
        return render_template('postform.html', product=product)
    
    # Handle GET request
    return render_template('postform.html')


@get_ps.route('/update/products/<int:product_id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def update_product(product_id):
    product = None
    from app import db, db_connection
    if request.method == "POST":
        ITEM_SKU = request.form["ITEM_SKU"]
        ITEM_NAME = request.form["ITEM_NAME"]
        ITEM_DESCRIPTION = request.form["ITEM_DESCRIPTION"]
        ITEM_PRICE = request.form["ITEM_PRICE"]
        ITEM_QTY = request.form["ITEM_QTY"]

        product = {
            "Item_SKU": ITEM_SKU,
            "Item_Name": ITEM_NAME,
            "Item_Description": ITEM_DESCRIPTION,
            "Item_Price": ITEM_PRICE,
            "Item_Qty": ITEM_QTY
        }

        conn = db_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
            UPDATE InventoryItem 
            SET Item_Name = %s, 
                Item_Description = %s, 
                Item_Price = %s, 
                Item_Qty = %s 
            WHERE Item_SKU = %s
            ''', (ITEM_NAME, ITEM_DESCRIPTION, ITEM_PRICE, ITEM_QTY, ITEM_SKU))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify({'error': 'Database error: ' + str(e)}), 500
        finally:
            cur.close()
            conn.close()
    return render_template('put.html', product=product)


@get_ps.route('/products/delete/<int:product_id>', methods=['DELETE'])
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


@get_ps.route('/products/delete', methods=['GET'])
@login_required
@role_required('admin')
def delete_product_page():
    return render_template('delete_product.html')

