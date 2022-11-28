from .exceptions import *
from booking_service.domain.customers.exceptions import *
from datetime import datetime
from booking_service.domain.customers.entities import Customer
from booking_service.domain.rooms.entities import Room
from .enums import BookingStatuses

class Booking(object):
    checkin: datetime
    checkout: datetime
    customer: Customer
    status: BookingStatuses
    margin: float
    room: Room
    id: int

    def __init__(self, checkin: datetime, checkout: datetime, customer: Customer):
        self.checkin = checkin
        self.checkout = checkout
        self.customer = customer
        self.status = BookingStatuses.OPEN
        self.id = None
    
    def create_booking(self):
        self.is_valid()
        self.status = BookingStatuses.RESERVED

    def delete_booking(self):
        self.is_valid()

        if self.status == BookingStatuses.CANCELED:
            raise BookingWithThisStatusCannotBeDeleted('Booking is in a status that does not allow delte')

        self.status = BookingStatuses.DELETED

    def update_booking(self):
        self.is_valid()

        if not self.id:
            raise BookingUpdateRequiresExistingBookingId('Cannot update a record without its Id')

    def is_valid(self):
        if self.checkin > self.checkout:
            raise CheckinDateCannotBeAfterCheckoutDate("Checkin cannot be after Checkout")
        elif not self.customer:
            raise CustomerCannotBeBlank("Customer is a required information")
    
        self.customer.is_valid()

        return True
