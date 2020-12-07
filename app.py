import os
import datetime
import math
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
def inventory_list():
    inventory = mongo.db.inventory.find()
    if request.method == "POST":
        matid = mongo.db.inventory.count()+1
        rgstmat = {
            "material_id": "%04d" % (matid,),
            "material_description": request.form.get("material_description"),
            "material_unit": request.form.get("material_unit")
        }
        mongo.db.inventory.insert_one(rgstmat)
        return redirect(url_for("inventory_list"))
    return render_template("inventory.html", inventory=inventory)


@app.route("/purchases")
def purchases():
    puorders = mongo.db.puorders.find()
    return render_template(
        "purchases.html", puorders=puorders)


@app.route("/material_info/<name>")
def material_info(name):
    puorders = mongo.db.puorders.find({"puo_items": name})
    level = mongo.db.inventory.find_one({"material_description": name})
    total = 0
    for mat in puorders:
        for qty in mat["puo_items_qty"]:
            total += int(qty)
    return render_template(
        "material_info.html",
        puorders=puorders,
        total=total,
        level=level["material_qty"])


@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    suppliers = mongo.db.suppliers.find()
    supplier_products = []
    supplier_products_price = []
    supplier_products_each = []
    if request.method == "POST":
        newsupplier = {
            "supplier_name": request.form.get("supplier_name"),
            "supplier_address": request.form.get("supplier_address"),
            "supplier_phone": request.form.get("supplier_phone"),
            "supplier_email": request.form.get("supplier_email"),
            "supplier_rep": request.form.get("supplier_rep"),
            "supplier_products": supplier_products,
            "supplier_products_price": supplier_products_price,
            "supplier_products_each": supplier_products_each,
        }
        mongo.db.suppliers.insert_one(newsupplier)
        return redirect(url_for("suppliers"))
    return render_template(
        "suppliers.html", suppliers=suppliers)


@app.route("/supplier_info/<supplier>")
def supplier_info(supplier):
    suppliers = mongo.db.suppliers.find_one({"supplier_name": supplier})
    return render_template(
        "supplier_info.html",
        suppliers=suppliers,
        items_list=zip(
            suppliers["supplier_products"],
            suppliers["supplier_products_price"],
            suppliers["supplier_products_each"]))


@app.route("/supplier_info/<supplier>/<item>/<price>/<each>")
def delete_item_supplier(supplier, item, price, each):
    mongo.db.suppliers.update(
        {"supplier_name": supplier},
        {"$pull":
            {
                "supplier_products": item,
                "supplier_products_price": price,
                "supplier_products_each": each}})
    return redirect(
        url_for("supplier_info", supplier=supplier))


@app.route("/supplier_info/<supplier>", methods=["GET", "POST"])
def edit_supplier(supplier):
    suppliers = mongo.db.suppliers.find_one({"supplier_name": supplier})
    edit_supplier = {
        "supplier_name": request.form.get("edit_supplier_name"),
        "supplier_address": request.form.get("edit_supplier_address"),
        "supplier_phone": request.form.get("edit_supplier_phone"),
        "supplier_email": request.form.get("edit_supplier_email"),
        "supplier_rep": request.form.get("edit_supplier_rep")
    }
    mongo.db.suppliers.update_one(
        {"supplier_name": supplier},
        {"$set": edit_supplier})
    return redirect(url_for("suppliers"))


@app.route("/supplier_info/<supplier>/<supplier_id>", methods=["GET", "POST"])
def delete_supplier(supplier, supplier_id):
    mongo.db.suppliers.remove({"_id": ObjectId(supplier_id)})
    return redirect(url_for("suppliers"))


@app.route("/new_purchase/<supplier>", methods=["GET", "POST"])
def new_purchase(supplier):
    suppliers = mongo.db.suppliers.find_one({"supplier_name": supplier})
    if request.method == "POST":
        date = datetime.datetime.now()
        puo = mongo.db.puorders.count()+1
        puo_items = request.form.get("new_purchase_items")
        puo_items_qty = request.form.get("new_purchase_qty")
        puo_items_price = request.form.get("new_purchase_cost")
        newpurchase = {
            "puo_number": "%04d" % (puo,),
            "puo_date": date.strftime("%x"),
            "puo_supplier": supplier,
            "puo_items": puo_items.split(","),
            "puo_items_qty": puo_items_qty.split(","),
            "puo_items_price": puo_items_price.split(","),
            "puo_total": format(
                float(request.form.get(
                    "new_purchase_total")), '.2f'),
            "puo_status": False,
        }
        mongo.db.puorders.insert_one(newpurchase)
        return redirect(url_for("purchases"))
    return render_template(
        "new_purchase.html",
        suppliers=suppliers,
        products_list=zip(
            suppliers["supplier_products"],
            suppliers["supplier_products_price"]))


@app.route("/select_supplier")
def select_supplier():
    suppliers = mongo.db.suppliers.find()
    return render_template(
        "select_supplier.html",
        suppliers=suppliers)


@app.route("/purchase_info/<puo_number>")
def purchase_info(puo_number):
    puorders = mongo.db.puorders.find_one({"puo_number": puo_number})
    suppliers = mongo.db.suppliers.find_one(
        {"supplier_name": puorders["puo_supplier"]})
    return render_template(
        "purchase_info.html",
        suppliers=suppliers,
        puorders=puorders,
        items_list=zip(
            puorders["puo_items"],
            puorders["puo_items_qty"],
            puorders["puo_items_price"]))


@app.route("/purchase_info/<puo_number>", methods=["GET", "POST"])
def items_received(puo_number):
    inventory = mongo.db.inventory.find()
    items_name = request.form.get("items_name").split(",")
    items_qty = request.form.get("items_qty").split(",")
    for i in inventory:
        for k in items_name:
            if k == i["material_description"]:
                newqty = (
                    int(i["material_qty"]) +
                    int(items_qty[items_name.index(k)]))
                mongo.db.inventory.update_one(
                    {"material_description": k},
                    {"$set": {"material_qty": newqty}})
    mongo.db.puorders.update_one(
        {"puo_number": puo_number},
        {"$set": {"puo_status": True}})
    return redirect(url_for("purchase_info", puo_number=puo_number))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
