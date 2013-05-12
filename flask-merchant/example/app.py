from flask import Flask, render_template, request
from flask.ext.merchant import get_gateway, get_integration, CreditCard
import os
import logging
import logging.handlers

curr_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config.from_pyfile(os.path.join(curr_dir, "settings.py"))

file_handler = logging.handlers.RotatingFileHandler('/tmp/flask.log') 
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

@app.route("/")
def main():
    return render_template("billing/main.html")

@app.route("/gateway/stripe/", methods=["GET", "POST"])
def s2s_stripe():
    with app.app_context():
        stripe = get_gateway("stripe")
        if request.method == 'POST':
            data = request.form.copy()
            credit_card = CreditCard(first_name=data.get("first_name"),
                                     last_name=data.get("last_name"),
                                     month=data.get("month"),
                                     year=data.get("year"),
                                     number=data.get("number"),
                                     verification_value=data.get("cvv"))
            amount = 1
            response = stripe.purchase(amount, credit_card)
        return render_template("billing/gateway/stripe.html")

@app.route("/offline/stripe/", methods=["GET", "POST"])
def stripe_js():
    with app.app_context():
        integration = get_integration("stripe_example")
        return render_template("billing/integration/stripe.html",
                               integration=integration)


if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=8000, debug=True)
    app.run(host="0.0.0.0", port=8000)
