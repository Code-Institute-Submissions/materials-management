import os
import datetime
import numpy
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
@app.route("/orders")
def orders():
    orders = mongo.db.orders.find()
    return render_template(
        "orders.html", orders=orders)


@app.route("/new_order", methods=["GET", "POST"])
def new_order():
    order_id = mongo.db.orders.count()+1
    products = mongo.db.products.find()
    customer = []
    if request.method == "POST":
        customer.append(request.form.get("customer_fname"))
        customer.append(request.form.get("customer_lname"))
        customer.append(request.form.get("customer_phone"))
        customer.append(request.form.get("customer_email"))
    return render_template(
        "new_order.html",
        order_id=order_id,
        products=products,
        customer=customer)


@app.route("/new_order/<order_id>", methods=["GET", "POST"])
def add_new_order(order_id):
    date = datetime.datetime.now()
    if request.method == "POST":
        order_items = request.form.get("new_product_items").split(",")
        order_items_qty = request.form.get("new_product_qty").split(",")
        neworder = {
            "order_id": order_id,
            "order_date": date.strftime("%x"),
            "order_status": "Pending",
            "order_items": order_items,
            "order_items_qty": order_items_qty,
            "customer_fname": request.form.get("customer_fname"),
            "customer_lname": request.form.get("customer_lname"),
            "customer_phone": request.form.get("customer_phone"),
            "customer_email": request.form.get("customer_email")
        }
    mongo.db.orders.insert_one(neworder)
    return redirect(url_for('orders'))


@app.route("/order_info/<order_id>")
def order_info(order_id):
    orders = mongo.db.orders.find_one({"order_id": order_id})
    in_stock = []
    status = True
    for j in range(0, len(orders["order_items"])):
        item = orders["order_items"][j]
        item_qty = int(orders["order_items_qty"][j])
        product = mongo.db.stock.find(
            {"product_name": item})
        for p in product:
            if int(p["product_qty"]) < item_qty:
                status = False
            in_stock.append(p["product_qty"])
    print(orders["order_status"])
    return render_template(
        "order_info.html",
        items=zip(
            orders["order_items"],
            orders["order_items_qty"],
            in_stock),
        orders=orders,
        order_id=order_id,
        status=status)


@app.route("/new_request/<prdorder_number>/<action>")
def new_request(prdorder_number, action):
    if action == "add":
        date = datetime.datetime.now()
        prdorders = mongo.db.prdorders.find_one({
            "prdorder_number": prdorder_number})
        products = mongo.db.products.find_one({
            "product_name": prdorders["prdorder_product"]})
        materials = list(numpy.unique(products["product_material_name"]))
        materials_qty = []
        for m in range(0, len(materials)):
            materials_qty.append(0)
            for i in range(0, len(products["product_material_name"])):
                if materials[m] == products["product_material_name"][i]:
                    materials_qty[m] += int(prdorders["prdorder_qty"])*int(
                        products["product_material_qty"][i])
        newrequest = {
            "matrequest_id": mongo.db.matrequest.count()+1,
            "matrequest_prdorder_id": prdorders["prdorder_number"],
            "matrequest_product": prdorders["prdorder_product"],
            "matrequest_date": date.strftime("%x"),
            "matrequest_status": "Pending",
            "matrequest_items": materials,
            "matrequest_items_qty": materials_qty
            }
        prdorder_history = prdorders["prdorder_history"]
        prdorder_history.append(
            "Materials Requested: "
            + date.strftime("%x")
            + " "
            + date.strftime("%X"))
        mongo.db.matrequest.insert_one(newrequest)
        mongo.db.prdorders.update(
            {"prdorder_number": prdorders["prdorder_number"]},
            {"$set": {
                "prdorder_status": "Materials Requested",
                "prdorder_history": prdorder_history
                }})
        return redirect(url_for(
            "production_order_info",
            name=prdorders["prdorder_product"],
            prdorder_number=prdorders["prdorder_number"]))
    return redirect(url_for(
        "production_order_info",
        name=prdorders["prdorder_product"],
        prdorder_number=prdorders["prdorder_number"]))


@app.route("/order_info/<order_id>/<status>")
def ship_order(order_id, status):
    orders = mongo.db.orders.find_one({"order_id": order_id})
    mongo.db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"order_status": "Shipped"}})
    for j in range(0, len(orders["order_items"])):
        item = orders["order_items"][j]
        item_qty = int(orders["order_items_qty"][j])
        product = mongo.db.stock.find_one(
            {"product_name": item})
        product_qty = int(product["product_qty"])
        balance = product_qty - item_qty
        mongo.db.stock.update_one(
            {"product_name": item},
            {"$set": {"product_qty": balance}})
    return redirect(url_for("order_info", order_id=order_id))


@app.route("/stock", methods=["GET", "POST"])
def stock():
    if request.method == "POST":
        prdorder_number = mongo.db.prdorders.count()+1
        date = datetime.datetime.now()
        prdorder = {
            "prdorder_number": "%04d" % (prdorder_number,),
            "prdorder_date": date.strftime("%x"),
            "prdorder_product": request.form.get("prdorder_product"),
            "prdorder_qty": request.form.get("prdorder_qty"),
            "prdorder_status": "Pending",
            "prdorder_history": [
                "Order created: "
                + date.strftime("%x")
                + " "
                + date.strftime("%X")]
        }
        mongo.db.prdorders.insert_one(prdorder)
        return redirect(url_for('production_orders'))
    stock = list(mongo.db.stock.find())
    orders = list(mongo.db.orders.find())
    products = []
    for s in stock:
        i = stock.index(s)
        products.append(0)
        for o in orders:
            for j in range(0, len(o["order_items"])):
                if s["product_name"] == o["order_items"][j]:
                    qty = int(o["order_items_qty"][j])
                    if o["order_status"] == "Pending":
                        products[i] += qty
    return render_template(
        "stock.html",
        stock=zip(stock, products))


@app.route("/production_orders")
def production_orders():
    prdorders = mongo.db.prdorders.find()
    return render_template(
        "production_orders.html", prdorders=prdorders)


@app.route(
    "/production_orders/<name>/<prdorder_number>", methods=["GET", "POST"])
def production_order_info(name, prdorder_number):
    products = mongo.db.products.find_one({"product_name": name})
    prdorders = mongo.db.prdorders.find_one(
        {"prdorder_number": prdorder_number})
    materials = list(numpy.unique(products["product_material_name"]))
    materials_qty = []
    materials_unit = []
    for m in range(0, len(materials)):
        materials_qty.append(0)
        for i in range(0, len(products["product_material_name"])):
            if materials[m] == products["product_material_name"][i]:
                materials_qty[m] += int(products["product_material_qty"][i])
                materials_unit.append(products["product_material_unit"][i])
    return render_template(
        "production_order_info.html",
        items=zip(
            materials,
            materials_qty,
            materials_unit),
        products=products,
        prdorders=prdorders)


@app.route("/materials_request")
def materials_request():
    matrequest = mongo.db.matrequest.find()
    return render_template(
        "materials_request.html", matrequest=matrequest)


@app.route("/materials_request_info/<matrequest_id>")
def materials_request_info(matrequest_id):
    request = mongo.db.matrequest.find_one(
        {"matrequest_id": int(matrequest_id)})
    print(request["matrequest_items"])
    in_inventory = []
    for m in range(0, len(request["matrequest_items"])):
        material = request["matrequest_items"][m]
        in_inventory.append(0)
        inventory = mongo.db.inventory.find_one(
            {"material_description": material})
        in_inventory[m] = inventory["material_qty"]
    return render_template(
        "materials_request_info.html",
        matrequest_id=request["matrequest_id"],
        items=zip(
            request["matrequest_items"],
            request["matrequest_items_qty"],
            in_inventory),
        request=request)


@app.route("/inventory", methods=["GET", "POST"])
def inventory_list():
    inventory = mongo.db.inventory.find()
    if request.method == "POST":
        matid = mongo.db.inventory.count()+1
        rgstmat = {
            "material_id": "%04d" % (matid,),
            "material_description": request.form.get("material_description"),
            "material_qty": 0,
            "material_unit": request.form.get("material_unit")
        }
        mongo.db.inventory.insert_one(rgstmat)
        return redirect(url_for("inventory_list"))
    return render_template("inventory.html", inventory=inventory)


@app.route("/products")
def products():
    products = mongo.db.products.find()
    return render_template(
        "products.html", products=products)


@app.route("/new_product/<product_type>", methods=["GET", "POST"])
def new_product(product_type):
    products = mongo.db.products.find()
    inventory = list(mongo.db.inventory.find())
    suppliers = list(mongo.db.suppliers.find())
    product_material_name = []
    product_material_qty = []
    product_material_unit = []
    if request.method == "POST":
        if product_type == "Product":
            sub_products = [request.form.get("new_product_name")]
            sub_products_qty = [1]
            product_pack = "Product"
            product_id = [0]
            product_material_name = request.form.get(
                "new_product_items").split(",")
            product_material_qty = request.form.get(
                "new_product_qty").split(",")
            for item in product_material_name:
                material = mongo.db.inventory.find_one({
                    "material_description": item})
                product_material_unit.append(material["material_unit"])
        else:
            sub_products = request.form.get("new_product_items").split(",")
            sub_products_qty = request.form.get("new_product_qty").split(",")
            product_pack = "Pack"
            product_id = request.form.get("new_product_id").split(",")
            for sp in product_id:
                material = mongo.db.products.find_one(
                    {"product_name": sub_products[int(sp)]})
                for i in material["product_material_name"]:
                    product_material_name.append(i)
                for i in material["product_material_qty"]:
                    q = i*int(sub_products_qty[int(sp)])
                    product_material_qty.append(q)
                for i in material["product_material_unit"]:
                    product_material_unit.append(i)
        new_product = {
            "product_name": request.form.get("new_product_name"),
            "product_cost": format(
                float(request.form.get(
                    "new_product_total")), '.2f'),
            "product_pack": product_pack,
            "sub_products": sub_products,
            "sub_products_qty": sub_products_qty,
            "product_material_name": product_material_name,
            "product_material_qty": product_material_qty,
            "product_material_unit": product_material_unit
        }
        mongo.db.products.insert_one(new_product)
        return redirect(url_for("products"))
    if product_type == "Product":
        return render_template(
            "new_product.html",
            product_type="Product",
            products=products,
            inventory=inventory,
            suppliers=suppliers)
    else:
        return render_template(
            "new_product.html",
            products=products,
            product_type="Pack")


@app.route("/product_info/<name>", methods=["GET", "POST"])
def product_info(name):
    products = mongo.db.products.find_one({"product_name": name})
    materials = list(numpy.unique(products["product_material_name"]))
    materials_qty = []
    materials_unit = []
    for m in range(0, len(materials)):
        materials_qty.append(0)
        for i in range(0, len(products["product_material_name"])):
            if materials[m] == products["product_material_name"][i]:
                materials_qty[m] += int(products["product_material_qty"][i])
                materials_unit.append(products["product_material_unit"][i])
    return render_template(
        "product_info.html",
        items=zip(
            materials,
            materials_qty,
            materials_unit),
        products=products)


@app.route("/purchases")
def purchases():
    puorders = mongo.db.puorders.find()
    return render_template(
        "purchases.html", puorders=puorders)


@app.route("/material_info/<name>", methods=["GET", "POST"])
def material_info(name):
    puorders = mongo.db.puorders.find({"puo_items": name})
    inventory = mongo.db.inventory.find_one({"material_description": name})
    supplier = mongo.db.suppliers.find()
    suppliers = list(mongo.db.suppliers.find({"supplier_products": name}))
    if request.method == "POST":
        supplier = request.form.get("supplier_name")
        mongo.db.suppliers.update(
            {"supplier_name": supplier},
            {"$push":
                {
                    "supplier_products": request.form.get(
                        "material_description"),
                    "supplier_products_price": request.form.get(
                        "supplier_products_price"),
                    "supplier_products_each": request.form.get(
                        "supplier_products_each")
                }}
        )
        return redirect(url_for("material_info", name=name))
    total = 0
    for order in puorders:
        if order["puo_status"] is False:
            for i in range(0, len(order["puo_items"])):
                total += int(order["puo_items_qty"][i])
    return render_template(
        "material_info.html",
        puorders=puorders,
        total=total,
        inventory=inventory,
        suppliers=suppliers,
        supplier=supplier)


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


@app.route("/supplier_info/<supplier>/<item>")
def delete_item_supplier(supplier, item):
    mongo.db.suppliers.update(
        {"supplier_name": supplier},
        {"$pull":
            {
                "supplier_products": item,
                }}
        )
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


@app.route("/supplier_info/<supplier>/<supplier_rep>/<supplier_id>")
def delete_supplier(supplier, supplier_rep, supplier_id):
    print(supplier_id)
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
            suppliers["supplier_products_price"],
            suppliers["supplier_products_each"]))


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


@app.route("/purchase_info/<puo_number>/<status>")
def items_received(puo_number, status):
    puorders = mongo.db.puorders.find_one({"puo_number": puo_number})
    for k in range(0, len(puorders["puo_items"])):
        item = puorders["puo_items"][k]
        inventory = mongo.db.inventory.find_one(
            {"material_description": item})
        qty = inventory["material_qty"]
        newqty = qty+int(puorders["puo_items_qty"][k])
        mongo.db.inventory.update_one(
            {"material_description": item},
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
