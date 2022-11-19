from datetime import datetime
from booking_service.domain.booking.entities import Booking
from booking_service.domain.customers.entities import Customer
from booking_service.application.customers.customer_dto import CustomerDto

class BookingDto(object):
    checkin: datetime
    checkout: datetime
    customer: Customer

    def __init__(self, checkin: datetime, checkout: datetime, customer: CustomerDto):
        self.checkin = checkin
        self.checkout = checkout
        self.customer = customer

    def to_domain(self):
        return Booking(self.checkin, self.checkout, self.customer)