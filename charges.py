from __main__ import app
from app import db
from app import ma
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from checkouts import Checkout

class Charge(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    checkout_id = db.Column(db.String(100))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))
    reference = db.Column(db.String(100))
    state = db.Column(db.String(30))

    def __init__(self, checkout_id, amount, currency, reference):
        self.id = 'ch-' + str(uuid.uuid4())
        self.checkout_id = checkout_id
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

    # creates a charge and captures the funds
    new_charge = Charge(checkout_id, amount, reference, currency)

    # marks the charged checkout id as completed
    checkout = Checkout.query.get(checkout_id)
    checkout.state = 'completed'

    db.session.add(new_charge)
    db.session.commit()

    return charge_schema.jsonify(new_charge)


@app.route('/charges/<id>', methods=['GET'])
def retrieve_charge(id):
    charge = Charge.query.get(id)
    if(charge == None):
        return jsonify({'Error': 'Cannot find charge with charge_id:' + id})
    else: 
        return charge_schema.jsonify(charge)