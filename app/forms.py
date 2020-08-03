from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DecimalField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Stock, Supplier
from flask_login import current_user

"""
This is the design for the login form, not a lot of validation is needed
as it's all performed when trying to log in.
"""
class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

"""
This is the registration form, there is some validation to ensure that there are no
duplicate usernames or emails getting entered into the database.
While it's not foolproof, it's unlikely that this site is going to get enough
traffic to fool these validators.
"""
class RegisterForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email Address", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", 
    validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already in use.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already in use.")

"""
This is the edit profile form, allowing the user to edit their username or email
if they want to. There's not a lot to edit because the user is not a part
of this project that I'm focusing very heavily on, so there's not a lot of information
to edit.
Again there are validators to ensure that no duplicates are entered into the database.
"""
class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Edit Account")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError("Email already in use.")

    def validate_username(self, username):
        if username.data != current_user.email:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("Username already in use.")

"""
This is the form to add a supplier. It offers both a name and a description for the supplier,
however the description is optional as it is not really relevant to anything apart from some
customisation and potential readability, 
but if we made it mandatory most would probably end up being full of nonsense and thus
would be a waste of time.
There is some validation to ensure that you cannot enter the same supplier name multiple times.
"""
class AddSupplier(FlaskForm):
    supplier_name = StringField("Supplier Name", validators = [DataRequired()])
    supplier_description = TextAreaField("Supplier Description", validators = [Length(min=0, max=500)])
    submit = SubmitField("Add Supplier")

    def validate_supplier_name(self, supplier_name):
        supplier_name = Supplier.query.filter_by(supplier_name=supplier_name.data).first()
        if supplier_name is not None:
            raise ValidationError("A supplier with this name has already been added to the database.")

"""
This is the form to add stock to the database, allowing a relational reference to
a supplier using the supplier_name field, which gets converted to the supplier_id
field in the routes.py file.
There is some validation to ensure that a product cannot be added twice, as each
supplier will call their product a slightly different name, and it also
ensures that the supplier actually exists before you can add a product that's related to it,
hopefully lessening any database errors.
"""
class AddStock(FlaskForm):
    product_name = StringField("Product Name", validators = [DataRequired()])
    supplier_name = StringField("Supplier", validators = [DataRequired()])
    product_price = StringField("Product Price", validators = [DataRequired()])
    current_stock = StringField("Current Stock")
    submit = SubmitField("Add Product")

    def validate_product_name(self, product_name):
        product_name = Stock.query.filter_by(product_name=product_name.data).first()
        if product_name:
            raise ValidationError("A product with this name already exists.")

    def validate_supplier_name(self, supplier_name):
        supplier_name = Supplier.query.filter_by(supplier_name=supplier_name.data).first()
        if supplier_name is None:
            raise ValidationError("There is no supplier with this name.")

"""
This is the form to edit the supplier, it is essentially exactly the same as the
add supplier form but has been recreated in order to keep code more readable and stop any 
issues that might arise from using the same form.
"""
class EditSupplier(FlaskForm):
    supplier_name = StringField("Supplier Name", validators = [DataRequired()])
    supplier_description = StringField("Supplier Description")
    submit = SubmitField
    
    def validate_supplier_name(self, supplier_name):
        supplier_name = Supplier.query.filter_by(supplier_name=supplier_name.data).first()
        if supplier_name is not None:
            raise ValidationError("A supplier with this name has already been added to the database.")

"""
This is the form to edit the stock, it is very similar to the add stock form but has been
duplicated for the same reasons as the edit supplier form.
"""
class EditStock(FlaskForm):
    product_name = StringField("Product Name", validators = [DataRequired()])
    supplier_name = StringField("Supplier", validators = [DataRequired()])
    product_price = StringField("Product Price", validators = [DataRequired()])
    current_stock = StringField("Current Stock")
    submit = SubmitField("Add Product")

    def validate_product_name(self, product_name):
        product_name = Stock.query.filter_by(product_name=product_name.data).first()
        if product_name:
            raise ValidationError("A product with this name already exists.")

    def validate_supplier_name(self, supplier_name):
        supplier_name = Supplier.query.filter_by(supplier_name=supplier_name.data).first()
        if supplier_name is None:
            raise ValidationError("There is no supplier with this name.")