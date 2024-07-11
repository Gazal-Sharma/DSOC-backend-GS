from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from utils import role_required
from flask_login import login_required, current_user

post_pd = Blueprint("post_pd", __name__, template_folder="templates")


@post_pd.route('/create/product', methods=['GET', 'POST'])
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