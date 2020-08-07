from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, EditProfileForm, AddSupplier, AddStock, EditStock, EditSupplier
from app.models import User, Stock, Supplier
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

@app.route("/")
@app.route("/index")
def index():
	stockData = Stock.query.all()
	if stockData is not None:
		return render_template("index.html", title = "Home", stock = stockData)
	else:
		return "There's no data to show."

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for("login"))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get("next")
		if next_page:
			return redirect(next_page)
		return redirect(url_for("index"))
	return render_template("users/login.html", title = "Sign In", form = form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congratulations, you're now a registered user!")
		return redirect(url_for("login"))
	return render_template("users/register.html", title="Register", form=form)

@app.route("/user/<username>")
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template("users/user.html", user=user)

@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Your changes have been saved.")
		return redirect(url_for("edit_profile"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template("users/edit-profile.html", title="Edit Profile", form=form)


# add stock page, hopefully including supplier ID through the supplier_name
@app.route("/add_stock", methods = ["GET", "POST"])
@login_required
def add_stock():
	form = AddStock()
	if form.validate_on_submit():
		# supplier_id_var = Supplier.query.filter_by(supplier_name = form.supplier_name.data).first()
		newstock = Stock(
			product_name = form.product_name.data,
			product_price = form.product_price.data,
			supplier = Supplier.query.filter_by(supplier_name = form.supplier_name.data).first(),
			current_stock = form.current_stock.data
		)
		db.session.add(newstock)
		db.session.commit()
		flash("Stock has been added.")
		return redirect(url_for("index"))
	return render_template("stock/add_stock.html", title = "Add Stock", form = form)

@app.route("/add_supplier", methods = ["GET", "POST"])
@login_required
def add_supplier():
	form = AddSupplier()
	if form.validate_on_submit():
		supplier = Supplier(
			supplier_name = form.supplier_name.data,
			supplier_description = form.supplier_description.data
		)
		db.session.add(supplier)
		db.session.commit()
		flash("Supplier has been added.")
		return redirect(url_for("add_supplier"))
	return render_template("suppliers/add_supplier.html", title = "Add Supplier", form = form)
# need to add validation so that I don't have to change my supplier name every time
@app.route("/edit_supplier/<supplier_id>", methods = ["GET", "POST"])
@login_required
def edit_supplier(supplier_id):
	supplier = Supplier.query.filter_by(supplier_id = supplier_id).first()
	form = EditSupplier()
	if form.validate_on_submit():
		supplier.supplier_name = form.supplier_name.data
		supplier.supplier_description = form.supplier_description.data
		db.session.commit()
		flash("Supplier has been updated.")
	elif request.method == "GET":
		form.supplier_name.data = supplier.supplier_name
		form.supplier_description.data = supplier.supplier_description
	return render_template("suppliers/edit_supplier.html", title = "Update Supplier", form = form)

# need to add validation so I don't have to change the product name every time
@app.route("/edit_product/<product_id>", methods = ["GET", "POST"])
@login_required
def edit_product(product_id):
	product = Stock.query.filter_by(product_id = product_id).first()
	form = EditStock()
	if form.validate_on_submit():
		product.product_name = form.product_name.data
		product.product_price = form.product_price.data
		product.supplier_name = form.supplier_name.data
		product.current_stock = form.current_stock.data
		db.session.commit()
		flash("Stock has been updated.")
		return redirect(url_for("edit_product", product_id = product_id))
	elif request.method == "GET":
		form.product_name.data = product.product_name
		form.product_price.data = product.product_price
		form.supplier_name.data = product.supplier.supplier_name
		form.current_stock.data = product.current_stock
	return render_template("stock/edit_product.html", title = "Update Stock", form = form)

# also need a view product which will show the indiviual product and allow you to edit it from there
@app.route("/product/<product_id>")
@login_required
def view_product(product_id):
	productData = Stock.query.filter_by(product_id = product_id).first()
	if productData is not None:
		return render_template("stock/view_product.html", title = "Product Info", stock = productData)
	else:
		return render_template("404.html")

@app.route("/supplier/<supplier_id>")
@login_required
def view_supplier(supplier_id):
	supplierData = Supplier.query.filter_by(supplier_id = supplier_id).first()
	supplierStock = Stock.query.filter_by(supplier_id = supplier_id).all()
	if supplierData is not None and supplierStock is not None:
		return render_template("suppliers/view_supplier.html", title = Supplier,  supplier = supplierData, stock = supplierStock)
	else:
		return render_template("404.html")


@app.route("/supplier/delete/<supplier_id>")
@login_required
def delete_supplier(supplier_id):
	if current_user.is_authenticated:
		supplier = Supplier.query.filter_by(supplier_id = supplier_id).first()
		supplierstock = Stock.query.filter_by(supplier_id = supplier_id).all()
		for stock in supplierstock:
			db.session.delete(stock)
		db.session.delete(supplier)
		db.session.commit()
		flash("Supplier and associated stock has been deleted.")
		return redirect(url_for("add_supplier"))

@app.route("/product/delete/<product_id>")
@login_required
def delete_product(product_id):
	if current_user.is_authenticated:
		product = Stock.query.filter_by(product_id = product_id).first()
		db.session.delete(product)
		db.session.commit
		flash("Stock has been deleted.")
		return redirect(url_for("add_stock"))