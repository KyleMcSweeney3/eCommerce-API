from tabnanny import check
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import random
import uuid

# Initialise flask app 
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# init marshmallow
ma = Marshmallow(app)

class Checkout(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(10))
    amount = db.Column(db.Float)
    state = db.Column(db.String(30))
    reference = db.Column(db.String(100))
    currency = db.Column(db.String(3))

    def __init__(self, first_name, last_name, email, phone_number, amount, reference, currency):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.amount = amount
        self.reference = reference
        self.currency = currency
        self.state = 'created'

# Checkout Schema
class CheckoutSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'amount', 'reference', 'currency', 'state')

# init schema
checkout_schema = CheckoutSchema()
checkouts_schema = CheckoutSchema(many=True)

# Create a checkout
@app.route('/checkouts', methods=['POST'])
def create_checkout():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    amount = request.json['amount']
    reference = request.json['reference']
    currency = request.json['currency']

    new_checkout = Checkout(first_name, last_name, email, phone_number, amount, reference, currency)

    db.session.add(new_checkout)
    db.session.commit()

    return checkout_schema.jsonify(new_checkout)

@app.route('/checkouts/<id>', methods=['GET'])
def retrieve_checkout(id):
    checkout = Checkout.query.get(id)
    if(checkout == None):
        return jsonify({'Error': 'Checkout does not exist'})
    else: 
        return checkout_schema.jsonify(checkout)

# helper endpoint to approve a checkout for charge 
@app.route('/checkouts/approve/<id>', methods=['PUT'])
def update_checkout(id):
    checkout = Checkout.query.get(id)

    checkout.state = 'approved'

    db.session.commit()

    return checkout_schema.jsonify(checkout)

class Charge(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    checkout_id = db.column(db.String(100))
    state = db.Column(db.String(100))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))
    reference = db.Column(db.String(100))
    state = db.Column(db.String(30))

    def __init__(self, checkout_id, amount, currency, reference):
        self.id = str(uuid.uuid4())
        self.checkout_id = checkout_id,
        self.amount = amount
        self.currency = currency
        self.reference = reference
        self.state = 'captured'

class ChargeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'checkout_id', 'amount', 'reference', 'currency', 'state')

charge_schema = ChargeSchema()
charges_schema = ChargeSchema(many=True)

@app.route('/charges', methods=['POST'])
def create_charge():
    checkout_id = request.json['checkout_id']
    amount = request.json['amount']
    reference = request.json['reference']
    currency = request.json['currency']

    new_charge = Charge(checkout_id, amount, reference, currency)

    db.session.add(new_charge)
    db.session.commit()

    return checkout_schema.jsonify(new_charge)

# Run server
if __name__ == '__main__':
    app.run(debug=True, port=5001)