# Debug Log

**Explain how you used the the techniques covered (Trace Forward, Trace Backward, Divide & Conquer) to uncover the bugs in each exercise. Be specific!**

In your explanations, you may want to answer:

- What is the expected vs. actual output?
- If there is a stack trace, what useful information does it contain?
- Which technique did you use, on which line numbers?
- What assumptions did you have about each line of code, and which ones were proven to be wrong?

_Example: I noticed that the program should show pizza orders once a new order is made, and that it wasn't showing any. So, I used the trace forward technique starting on line 13. I discovered the bug on line 27 was caused by a typo of 'pzza' instead of 'pizza'._

_Then I noticed another bug ..._

## Exercise 1
#### Error 1
_EXPECTED: When a pizza order is submitted through the order form, it should redirect to the home page and show the pizza order on the homepage_ </br>
_ACTUAL: When submitting the form, an error is thrown that says the following `TypeError: 'topping' is an invalid keyword argument for PizzaTopping` which originates from line 96 in the function `pizza_order_submit` in app.py_
- On line 96, we assume that we add a pizza topping from the PizzaTopping model, which has the attribute `topping_type` and not just `topping`
- Changing to the correct spelling format fixed the bug </br>

#### Error 2
_EXPECTED: When a pizza order is submitted through the order form, it should redirect to the home page and show the pizza order on the homepage_ </br>
_ACTUAL: When form is submitted, a URL endpoint build error is thrown `werkzeug.routing.BuildError: Could not build url for endpoint '/'. Did you mean 'fulfill_order' instead?`_
- `url_for` takes in a function name of a route, not the route itself
- changing to the name of the route function (home) fixed it </br>

#### Error 3
_EXPECTED: When a pizza order is submitted through the order form, it should redirect to the home page and show the pizza order on the homepage_ </br>
_ACTUAL: The pizza order is not showing on the home page, but the flash is there which means the `pizza_order_submit` function ran all the way through_
- I first checked that the home page query was correct and was accessing pizza attributes correctly
- Then, I checked all routes, especially the route that does the POST request to /order
- We assume this function creates a pizza object from the data in the submitted form, so I checked the form to see if the data was loading in correctly
- Once I confirmed that, I checked the functionality of submitting to the database
- We assume that a pizza is added to the database, and the change is committed
- `db.session.commit()` is never called, so that is the error
- This threw another error `sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: pizza.order_name` and it showed that it was attempting to insert `(None, None, 'THIN', 0) as (order_name, size, crust_type, fulfilled)`
- This meant that the attribute weren't actually being inserted into the Pizza object
- When checking all form data, the `request.form.get` attribute names were not correct (`name` is supposed to be `order_name`, `size` is supposed to be `pizza_size`) </br>

#### Error 4
_EXPECTED: When a pizza order is submitted through the order form, it should redirect to the home page and show the CORRECT pizza order on the homepage_ </br>
_ACTUAL: It shows the pizza with all available toppings_
- The toppings are added in the for loop on line 94, which loops through each topping type
- The toppings_list data from the form is also never accessed
- This makes us assume that the toppings are never accessed and added to the pizza
- Let's try to create an if statement to check if the topping is in the toppings_list from the form
- First, we assume the toppings_list is in fact a list. It is not, when clicking on multiple toppings, it returns this `('toppings', 'SOY_CHEESE'), ('toppings', 'ONIONS'), ('toppings', 'SPINACH')` and when using `request.form.get`, it just returns the first instance of toppings.
- Let's check the html form, it looks good
- It seems that `get` just gets the first thing it sees, but we need to use `getlist` instead to get all the things with that attribute name of toppings
- Now we have a list, let's add the if statement in the toppings loop. That didn't work, let's think about it in a different way
- We can use the number instead of the name for the `PizzaTopping` object as well, so let's instead loop through the topping list we get through the form, and then get the number for that topping using `ToppingType[topping]` </br>

_**And we're done!**_

## Exercise 2

[[Your answer goes here!]]

## Exercise 3

[[Your answer goes here!]]
