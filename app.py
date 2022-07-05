from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
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

import checkouts
import charges
import refunds

# Run server
if __name__ == '__main__':
    app.run(debug=True, port=5001)