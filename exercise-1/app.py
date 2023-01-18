from flask import Flask, flash, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

###############################################
### MODELS
###############################################

class PizzaSize(enum.Enum):
    SMALL = '12 Inch'
    MEDIUM = '16 Inch'
    LARGE = '20 Inch'

class CrustType(enum.Enum):
    THIN = 'Thin'
    THICK = 'Thick'
    GLUTEN_FREE = 'Gluten Free'

class ToppingType(enum.Enum):
    SOY_CHEESE = 'Soy Cheese'
    MUSHROOMS = 'Mushrooms'
    ONIONS = 'Onions'
    SPINACH = 'Spinach'
    PINEAPPLE = 'Pineapple'

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(80), unique=False, nullable=False)
    size = db.Column(db.Enum(PizzaSize), nullable=False)
    crust_type = db.Column(db.Enum(CrustType), nullable=False)
    toppings = db.relationship('PizzaTopping')
    fulfilled = db.Column(db.Boolean, default=False)

class PizzaTopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topping_type = db.Column(db.Enum(ToppingType))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

with app.app_context():
    db.create_all()

###############################################
### ROUTES
###############################################

@app.route('/')
def home():
    # we assume this returns all pizza orders (index) NOT fulfilled from the database using the pizza model
    # we assume there is a fulfilled attribute in pizza model
    all_pizzas = Pizza.query.filter_by(fulfilled=False)

    print(all_pizzas)
    print(f'Num of pizzas: {all_pizzas.count()}')

    # we assume the pizza_orders is used in the jinja template called 'home.html'
    return render_template('home.html', pizza_orders=all_pizzas)

@app.route('/order', methods=['GET'])
def pizza_order_form():
    # we assume this returns the order.html jinja template and passes in sizes, crust_types, and toppings objects
    return render_template(
        'order.html',
        sizes=PizzaSize,
        crust_types=CrustType,
        toppings=ToppingType)

@app.route('/order', methods=['POST'])
def pizza_order_submit():
    # we assume this creates a pizza object from the submitted form data
    print(f'Form data: {request.form}')
    order_name = request.form.get('order_name')
    pizza_size_str = request.form.get('pizza_size')
    crust_type_str = request.form.get('crust_type')
    toppings_list = request.form.getlist('toppings')
    
    print(f'Pizza Data: {order_name}, {pizza_size_str}, {crust_type_str}, {toppings_list}\n')
    # we assume pizza model has attributes of order-name, size, crust_type, and toppings
    pizza = Pizza(
        order_name=order_name,
        size=pizza_size_str,
        crust_type=crust_type_str)
    
    print(pizza)
    print(pizza.size)

    # we assume this appends the toppings
    print('TOPPINGS START')
    print(f'Toppings list is list: {isinstance(toppings_list, list)}')
    for topping_str in toppings_list:
        # this looks like it is just appending all toppings? the topping list is not accessed from attributes above
        topping_enum = ToppingType[topping_str]
        print(topping_enum)
        # ERROR HERE
        # TypeError: 'topping' is an invalid keyword argument for PizzaTopping
        # there is no attribute called topping, but there is one called topping_type as so:
            # topping_type = db.Column(db.Enum(ToppingType))
        # let's replace topping with topping_type
        print(f'Final topping: {PizzaTopping(topping_type=topping_enum)}')
        pizza.toppings.append(PizzaTopping(topping_type=topping_enum))

    # adds pizza to session
    db.session.add(pizza)
    # ERROR, does not commit to session
    # needs:
    db.session.commit()

    # we assume this flashes a success message and redirects to the home page
    flash('Your order has been submitted!')
    return redirect(url_for('home'))


@app.route('/fulfill', methods=['POST'])
def fulfill_order():
    # we assume this changes the pizza fulfilled attribute from False to True
    pizza_id = request.form.get('pizza_id')
    pizza = Pizza.query.filter_by(id=pizza_id).one()

    pizza.fulfilled = True
    db.session.add(pizza)
    db.session.commit()
    
    flash(f'The order for {pizza.order_name} has been fulfilled.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)