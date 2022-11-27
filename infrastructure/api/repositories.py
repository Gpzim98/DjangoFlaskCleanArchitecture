import sys
sys.path.append('..')
sys.path.append('../..')
from booking_service.application.booking.booking_storage import BookingStorage
from booking_service.application.booking.booking_manager import BookingManager
from booking_service.application.booking.booking_dto import CustomerDto, BookingDto, UserDto
from .models import Booking, User, db, Customer

class BookingRepository(BookingStorage):
    def __init__(self):
        self.db = db

    def save_booking(self, bookingDto: BookingDto):
        pass

    def get_booking_by_id(self, id) -> BookingDto:
        pass

    def update_booking(self, booking_dto: BookingDto):
        pass

    def delete_booking(self, booking_dto: BookingDto):
        pass

    def _model_to_dto(self, booking: Booking, customer: Customer):
        customer_dto = CustomerDto(customer.name, customer.age, customer.document, customer.email)
        booking_dto = BookingDto(booking.checkin, booking.checkout, customer_dto)
        booking_dto.id = booking.id
        booking_dto.status = booking.status
        return booking_dto

    def get_all_bookings(self):
        bookings = Booking.query.all()
        bookings_dto = []
        for booking in bookings:
            customer = Customer.query.filter_by(id=booking.customer_id).first()
            bookings_dto.append(self._model_to_dto(booking, customer))
        return bookings_dto

    def get_filtered_bookings(self):
        bookings = Booking.query.filter(Booking.status.notin_(['CANCELED']))
        bookings_dto = []
        for booking in bookings:
            customer = Customer.query.filter_by(id=booking.customer_id).first()
            bookings_dto.append(self._model_to_dto(booking, customer))
        return bookings_dto


class UserRepository(object):
    def get_user(self, username, password):
        return User.query.filter_by(username=username, password=password).first()
