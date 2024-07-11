# from flask import Blueprint, render_template, jsonify, request


# put_pd = Blueprint("put_pd", __name__, template_folder = "templates")

# @put_pd.route('/update/products/<int:product_id>', methods = ['PUT','POST'])
# def update_product(product_id):
#     if request.method == "POST":
#         product_id = request.form["product_id"]
#         ITEM_SKU = request.form["ITEM_SKU"]
#         ITEM_NAME = request.form["ITEM_NAME"]
#         ITEM_DESCRIPTION = request.form["ITEM_DESCRIPTION"]
#         ITEM_PRICE = request.form["ITEM_PRICE"]
#         ITEM_QTY = request.form["ITEM_QTY"]

#         product = {
#             "Item_SKU": ITEM_SKU,
#             "Item_Name": ITEM_NAME,
#             "Item_Description": ITEM_DESCRIPTION,
#             "Item_Price": ITEM_PRICE,
#             "Item_Qty": ITEM_QTY
#         }

#         from app import db, db_connection
#         conn = db_connection()
#         cur = conn.cursor()
#         try:
#             cur.execute('''
#             UPDATE InventoryItem 
#             SET Item_Name = %s, 
#                 Item_Description = %s, 
#                 Item_Price = %s, 
#                 Item_Qty = %s 
#             WHERE Item_SKU = %s
#             ''', (ITEM_SKU, ITEM_NAME, ITEM_DESCRIPTION, ITEM_PRICE, ITEM_QTY, product_id))
#             conn.commit()
#         except Exception as e:
#             conn.rollback()
#             return jsonify({'error': 'Database error: ' + str(e)}), 500
#         finally:
#             cur.close()
#             conn.close()
#     return render_template('put_.html', product = product)
#     cur.close()
#     conn.close()
from flask import Blueprint, render_template, jsonify, request
from utils import role_required
from flask_login import login_required, current_user

put_pd = Blueprint("put_pd", __name__, template_folder="templates")

@put_pd.route('/update/products/<int:product_id>', methods=['GET', 'POST'])
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


