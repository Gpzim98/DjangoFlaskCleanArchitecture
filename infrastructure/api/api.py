from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '7SIDFYDS7FYSFI7BKJBIU4BF344JKF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db = SQLAlchemy(app)
app.app_context().push()
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'] 
        if not token:
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        
        return f(*args, **kwargs)
    return decorated

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean())

@app.route('/login')
def login():
    auth = request.authorization
    if auth:
        user = User.query.filter_by(username=auth.username, password=auth.password).first()
        if user:
            data = {'user': auth.username, 'is_admin': user.is_admin, 'exp': datetime.utcnow() + timedelta(minutes=30)}
            token = jwt.encode(data, app.config['SECRET_KEY']) 
            return {'token': token}
    return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/")
def hello_world():
    return {'message': 'Hello world'}

@app.route('/bookings')
@token_required
def bookings():
    return {'Bookings': 'Some bookings here'}