from .exceptions import CheckinDateCannotBeAfterCheckoutDate, CustomerCannotBeBlank
from booking_service.domain.customers.exceptions import *
from datetime import datetime
from booking_service.domain.customers.entities import Customer
from booking_service.domain.rooms.entities import Room
from enum import Enum

class BookingStatuses(Enum):
    OPEN = 0
    RESERVED = 1 
    FINISHED = 2
    CANCELED = 3

class Booking(object):
    checkin: datetime
    checkout: datetime
    customer: Customer
    status: BookingStatuses
    margin: float
    room: Room

    def __init__(self, checkin: datetime, checkout: datetime, customer: Customer):
        self.checkin = checkin
        self.checkout = checkout
        self.customer = customer
        self.status = BookingStatuses.OPEN
    
    def create_booking(self):
        self.is_valid()
        self.status = BookingStatuses.RESERVED

    def is_valid(self):
        if self.checkin > self.checkout:
            raise CheckinDateCannotBeAfterCheckoutDate("Checkin cannot be after Checkout")
        elif not self.customer:
            raise CustomerCannotBeBlank("Customer is a required information")
    
        self.customer.is_valid()

        return True
