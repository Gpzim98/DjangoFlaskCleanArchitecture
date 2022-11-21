from datetime import datetime
from booking_service.domain.booking.entities import Booking
from booking_service.application.customers.customer_dto import CustomerDto

class BookingDto(object):
    checkin: datetime
    checkout: datetime
    customer: CustomerDto
    status: str

    def __init__(self, checkin: datetime, checkout: datetime, customer: CustomerDto):
        self.checkin = checkin
        self.checkout = checkout
        self.customer = customer

    def to_domain(self):
        return Booking(self.checkin, self.checkout, self.customer.to_domain())

    def to_dto(self, booking: Booking):
        customer_dto = self.customer.to_dto(booking.customer)
        booking_dto = BookingDto(
            checkin=booking.checkin, 
            checkout=booking.checkout, 
            customer=customer_dto)
        booking_dto.status = booking.status.name
        return booking_dto

class UserDto(object):
    name: str
    is_admin: bool

    def __init__(self, name: str, is_admin: bool) -> None:
        self.name = name
        self.is_admin = is_admin

