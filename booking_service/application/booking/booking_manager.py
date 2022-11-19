from booking_service.domain.booking.exceptions import CheckinDateCannotBeAfterCheckoutDate, CustomerCannotBeBlank
from .booking_dto import BookingDto
from booking_service.domain.booking.enums import ErrorCodes

class BookingManager(object):
    def create_new_booking(self, bookingDto: BookingDto):
        domain_object = bookingDto.to_domain()

        try:
            if domain_object.is_valid():
                return 'save'
        except CheckinDateCannotBeAfterCheckoutDate as e:
            return {'message': e.message, 'code': ErrorCodes.CHECKINAFTERCHECKOUT}
        except CustomerCannotBeBlank as e:
            return {'message': e.message, 'code': ErrorCodes.CUSTOMERISREQUIRED}
        except Exception as e:
            return {'message': e.message, 'code': ErrorCodes.UNDEFINED}
