from booking_service.application.booking.booking_storage import BookingStorage
from booking_service.application.booking.booking_dto import BookingDto
from booking_service.application.customers.customer_dto import CustomerDto
from .models import Customer, Booking
from django.db import transaction

class BookingRepository(BookingStorage):
    def _customer_dto_to_model(self, customerDto: CustomerDto):
        customer = Customer()
        customer.name = customerDto.name
        customer.age = customerDto.age
        customer.document = customerDto.document
        customer.email = customerDto.email

        return customer

    def _booking_dto_to_model(self, booking_dto: BookingDto):
        booking = Booking()
        booking.checkin = booking_dto.checkin
        booking.checkout = booking_dto.checkout
        booking.status = booking_dto.status
        return booking

    @transaction.atomic
    def save_booking(self, booking_dto: BookingDto):
        customer = self._customer_dto_to_model(booking_dto.customer)
        customer.save()
        booking = self._booking_dto_to_model(booking_dto)
        booking.customer = customer
        booking.save()
