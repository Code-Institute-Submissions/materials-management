import os
import datetime
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
    suppliers = mongo.db.suppliers.find()
    return render_template(
        "purchases.html",
        orders=zip(puorders, suppliers))


@app.route("/new_purchase/<selected_supplier>", methods=["GET", "POST"])
def new_purchase(selected_supplier):
    supplier = selected_supplier
    suppliers = mongo.db.suppliers.find()
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
        flash("Purchase Order Processed")
        return redirect(url_for("purchases"))
    products_list = []
    price_list = []
    for i in suppliers:
        if i["supplier_name"] == selected_supplier:
            address = i["supplier_address"]
            phone = i["supplier_phone"]
            email = i["supplier_email"]
            rep = i["supplier_rep"]
            for j in i["supplier_products"]:
                products_list.append(j)
            for j in i["supplier_products_price"]:
                price_list.append(j)
    return render_template(
        "new_purchase.html",
        supplier=supplier,
        address=address,
        phone=phone,
        email=email,
        rep=rep,
        products_list=zip(
            products_list, price_list))


@app.route("/select_supplier", methods=["GET", "POST"])
def select_supplier():
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
        return redirect(url_for("select_supplier"))
    return render_template(
        "select_supplier.html",
        suppliers=suppliers)


@app.route("/see_purchase/<puo_number>")
def see_purchase(puo_number):
    puonumber = puo_number
    puorders = mongo.db.puorders.find()
    suppliers = mongo.db.suppliers.find()
    itemlist = []
    items = []
    qty = []
    price = []
    for i in puorders:
        if i["puo_number"] == puonumber:
            date = i["puo_date"]
            total = i["puo_total"]
            status = i["puo_status"]
            supplier = i["puo_supplier"]
            for j in i["puo_items"]:
                itemlist.append(len(itemlist)+1)
            for j in i["puo_items"]:
                items.append(j)
            for j in i["puo_items_qty"]:
                qty.append(int(j))
            for j in i["puo_items_price"]:
                price.append(float(j))
    for i in suppliers:
        if i["supplier_name"] == supplier:
            address = i["supplier_address"]
            phone = i["supplier_phone"]
            email = i["supplier_email"]
            rep = i["supplier_rep"]
    return render_template(
        "see_purchase.html",
        supplier=supplier,
        address=address,
        phone=phone,
        email=email,
        rep=rep,
        date=date,
        total=total,
        status=status,
        puonumber=puonumber,
        items_list=zip(
            itemlist,
            items, qty,
            price))


@app.route("/select_supplier/<the_supplier>")
def selected_supplier(the_supplier):
    the_supplier = the_supplier
    return redirect(url_for("new_purchase", selected_supplier=the_supplier))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
