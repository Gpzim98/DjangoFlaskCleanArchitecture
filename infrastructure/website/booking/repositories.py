from booking_service.application.booking.booking_storage import BookingStorage
from booking_service.application.booking.booking_dto import BookingDto
from booking_service.application.customers.customer_dto import CustomerDto
from booking_service.domain.booking.enums import BookingStatuses
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

    def _model_to_dto(self, booking: Booking):
        customer_dto = CustomerDto(
            booking.customer.name, 
            booking.customer.age, 
            booking.customer.document, 
            booking.customer.email)
        booking_dto = BookingDto(booking.checkin, booking.checkout, customer_dto)
        booking_dto.status = booking.status
        return booking_dto

    @transaction.atomic
    def save_booking(self, booking_dto: BookingDto):
        customer = self._customer_dto_to_model(booking_dto.customer)
        customer.save()
        booking = self._booking_dto_to_model(booking_dto)
        booking.customer = customer
        booking.save()

    def get_all_bookings(self):
        bookings = Booking.objects.all()
        bookings_dto = []
        for booking in bookings:
            bookings_dto.append(self._model_to_dto(booking))
        return bookings_dto

    def get_filtered_bookings(self):
        bookings = Booking.objects.exclude(status=BookingStatuses.CANCELED.name)
        bookings_dto = []
        for booking in bookings:
            bookings_dto.append(self._model_to_dto(booking))
        return bookings_dto

