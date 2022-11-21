from abc import ABC, abstractclassmethod
from .booking_dto import BookingDto

class BookingStorage(ABC):
    
    @abstractclassmethod
    def save_booking(self, bookingDto: BookingDto):
        pass

    @abstractclassmethod
    def get_all_bookings(self):
        pass

    @abstractclassmethod
    def get_filtered_bookings(self):
        pass
