import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/inventory", methods=["GET", "POST"])
def register_material():
    inventory = mongo.db.inventory.find()
    if request.method == "POST":
        matid = mongo.db.inventory.count()+1
        rgstmat = {
            "material_id": "%04d" % (matid,),
            "material_description": request.form.get("material_description"),
            "material_unit": request.form.get("material_unit"),
            "material_cost": request.form.get("material_cost")
        }
        mongo.db.inventory.insert_one(rgstmat)
        return redirect(url_for("register_material"))
    return render_template("inventory.html", inventory=inventory)


@app.route("/inventory/<material_id>")
def delete_material(material_id):
    mongo.db.inventory.remove(
        {"_id": ObjectId(material_id)})
    return redirect(url_for("register_material"))


@app.route("/purchases")
def purchases():
    puorders = mongo.db.puorders.find()
    inventory = mongo.db.inventory.find()
    suppliers = mongo.db.suppliers.find()
    return render_template(
        "purchases.html",
        puorders=puorders, inventory=inventory, suppliers=suppliers)


@app.route("/new_purchase/<selected_supplier>", methods=["GET", "POST"])
def new_purchase(selected_supplier):
    supplier = selected_supplier
    suppliers = mongo.db.suppliers.find()
    if request.method == "POST":
        puo = mongo.db.puorders.count()+1
        newpurchase = {
            "puo_number": puo,
            "puo_date": 'today',
            "puo_supplier": supplier,
            "puo_items": request.form.get("new_purchase_items"),
            "puo_items_qty": request.form.get("new_purchase_qty"),
            "puo_items_price": request.form.get("new_purchase_cost"),
            "puo_total": request.form.get("new_purchase_total"),
            "puo_status": False,
        }
        mongo.db.puorders.insert_one(newpurchase)
        flash("Purchase Order Processed")
        return redirect(url_for("new_purchase", selected_supplier=supplier))
    products_list = []
    price_list = []
    for i in suppliers:
        if i["supplier_name"] == selected_supplier:
            for j in i["supplier_products"]:
                products_list.append(j)
            for j in i["supplier_products_price"]:
                price_list.append(j)
    return render_template(
        "new_purchase.html", supplier=supplier,
        products_list=zip(products_list, price_list))


@app.route("/new_purchase_copy")
def new_purchase_copy():
    suppliers = mongo.db.suppliers.find()
    return render_template(
        "new_purchase_copy.html",
        suppliers=suppliers)


@app.route("/new_purchase_copy/<the_supplier>")
def selected_supplier(the_supplier):
    the_supplier = the_supplier
    return redirect(url_for("new_purchase", selected_supplier=the_supplier))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
