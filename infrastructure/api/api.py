from flask import Flask, make_response, request, session
import jwt
from datetime import datetime, timedelta
from .models import db
from .repositories import BookingRepository, UserRepository, BookingManager, UserDto, BookingDto, CustomerDto
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '7SIDFYDS7FYSFI7BKJBIU4BF344JKF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
db.init_app(app)

app.app_context().push()
# db.create_all()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        if not token:
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            session['current_user'] = {'user': data['user'], 'is_admin': data['is_admin']}
        except:
            return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        
        return f(*args, **kwargs)
    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if auth:
        rep  = UserRepository()
        user = rep.get_user(auth.username, auth.password)
        if user:
            data = {'user': auth.username, 'is_admin': user.is_admin, 'exp': datetime.utcnow() + timedelta(minutes=90)}
            token = jwt.encode(data, app.config['SECRET_KEY']) 
            return {'token': token}
    return make_response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/")
def hello_world():
    return {'message': 'Hello world'}

@app.route('/bookings')
@token_required
def bookings():
    repository = BookingRepository()
    manager = BookingManager(repository)
    user_dto = UserDto(session['current_user']['user'], session['current_user']['is_admin'])

    bookings = manager.get_bookings(user_dto)
    return get_serializable_booking_list(bookings)


@app.route('/create-booking', methods=['POST'])
@token_required
def create_booking():
    data = request.get_json()
    checkin = datetime.strptime(data['checkin'],  "%Y-%m-%dT%H:%M")
    checkout = datetime.strptime(data['checkout'],"%Y-%m-%dT%H:%M")

    customer_dto = get_customer_dto_from_request(data)

    booking_dto = BookingDto(checkin, checkout, customer_dto)
    repository = BookingRepository()
    manager = BookingManager(repository)
    resp = manager.create_new_booking(booking_dto)

    if resp['code'] == 'SUCCESS':
        return make_response(resp, 201)
    
    return make_response(resp, 400)

@app.route('/delete-booking/<id>', methods=['DELETE'])
@token_required
def delete_booking(id):
    repository = BookingRepository()
    manager = BookingManager(repository)
    resp = manager.delete_booking(id)
    
    if resp['code'] == 'SUCCESS':
        return make_response(resp, 201)
    
    return make_response(resp, 400)

def get_customer_dto_from_request(data):
    name = data['name']
    age = int(data['age'])
    document = data['document']
    email = data['email']
    return CustomerDto(name, age, document, email)

def get_serializable_booking_list(bookings):
    booking_list = []
    for booking in bookings:
        b = {
                'id': booking.id, 
                'checkin': booking.checkin, 
                'checkout': booking.checkout,
                'customer_id': booking.customer.id,
                'customer_name': booking.customer.name,
                'status': booking.status
            }
        booking_list.append(b)
    return booking_list