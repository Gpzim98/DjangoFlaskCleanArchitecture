from abc import ABC, abstractclassmethod
from .booking_dto import BookingDto

class BookingStorage(ABC):
    
    @abstractclassmethod
    def save_booking(self, bookingDto: BookingDto):
        pass
