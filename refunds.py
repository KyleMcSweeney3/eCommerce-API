from __main__ import app
from app import db
from app import ma
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from charges import Charges

class Refunds(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    charge_id = db.Column(db.String(100))
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))
    reference = db.Column(db.String(100))
    state = db.Column(db.String(30))

    def __init__(self, charge_id, amount, currency, reference):
        self.id = 'ch-' + str(uuid.uuid4())
        self.checkout_id = checkout_id
        self.amount = amount
        self.currency = currency
        self.reference = reference
        self.state = 'captured'

class RefundSchema(ma.Schema):
    class Meta:
        fields = ('id', 'charge_id', 'amount', 'reference', 'currency', 'state')

refund_schema = RefundSchema()
refunds_schema = RefundSchema(many=True)

@app.route('/refunds', methods=['POST'])
def create_refund():
    charge_id = request.json['checkout_id']
    amount = request.json['amount']
    reference = request.json['reference']
    currency = request.json['currency']

    # creates a charge and captures the funds
    new_refund = Refund(charge_id, amount, reference, currency)

    # marks the charged checkout id as completed
    charge = Charge.query.get(charge_id)
    charge.state = 'refunded'

    db.session.add(new_refund)
    db.session.commit()

    return refund_schema.jsonify(new_refund)

@app.route('/refunds/<id>', methods=['GET'])
def retrieve_refund(id):
