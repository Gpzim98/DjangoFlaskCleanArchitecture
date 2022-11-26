from datetime import datetime
from booking_service.domain.booking.entities import Booking
from booking_service.application.customers.customer_dto import CustomerDto
from booking_service.domain.booking.enums import BookingStatuses

class BookingDto(object):
    id: int
    checkin: datetime
    checkout: datetime
    customer: CustomerDto
    status: str

    def __init__(self, checkin: datetime, checkout: datetime, customer: CustomerDto):
        self.checkin = checkin
        self.checkout = checkout
        self.customer = customer
        self.id = None
        self.status = BookingStatuses.OPEN.name

    def to_domain(self):
        booking = Booking(self.checkin, self.checkout, self.customer.to_domain())
        booking.id = self.id
        booking.status = BookingStatuses[self.status]
        return booking

    def to_dto(self, booking: Booking):
        customer_dto = self.customer.to_dto(booking.customer)
        booking_dto = BookingDto(
            checkin=booking.checkin, 
            checkout=booking.checkout, 
            customer=customer_dto)
        booking_dto.status = booking.status.name
        booking_dto.id = booking.id
        return booking_dto

class UserDto(object):
    id: int
    name: str
    is_admin: bool

    def __init__(self, name: str, is_admin: bool) -> None:
        self.name = name
        self.is_admin = is_admin

