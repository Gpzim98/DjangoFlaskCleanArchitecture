from booking_service.domain.booking.exceptions import *
from booking_service.domain.customers.exceptions import *
from .booking_dto import BookingDto
from booking_service.domain.booking.enums import *
from .booking_storage import BookingStorage

class BookingManager(object):
    storage: BookingStorage

    def __init__(self, storage: BookingStorage) -> None:
        self.storage = storage

    def create_new_booking(self, bookingDto: BookingDto):
        booking_aggregate = bookingDto.to_domain()

        try:
            booking_aggregate.create_booking()
            final_dto = bookingDto.to_dto(booking_aggregate)
            self.storage.save_booking(final_dto)
            return {'message': SuccessCodes.SUCCESS.value, 'code': SuccessCodes.SUCCESS.name}
        except CheckinDateCannotBeAfterCheckoutDate as e:
            return {'message': ErrorCodes.CHECKINAFTERCHECKOUT.value, 'code': ErrorCodes.CHECKINAFTERCHECKOUT.name}
        except CustomerCannotBeBlank as e:
            return {'message': ErrorCodes.CUSTOMERISREQUIRED.value, 'code': ErrorCodes.CUSTOMERISREQUIRED.name}
        except CustomerShouldBeOlderThan18 as e:
            return {'message': ErrorCodes.CUSTOMERSHOULDBEOLDERTHAN18.value, 'code': ErrorCodes.CUSTOMERSHOULDBEOLDERTHAN18.name}
        except InvalidCustomerDocumentException as e:
            return {'message': ErrorCodes.INVALIDCUSTOMERDOCUMENT.value, 'code': ErrorCodes.INVALIDCUSTOMERDOCUMENT.name}
        except Exception as e:
            return {'message': ErrorCodes.UNDEFINED.value, 'code': ErrorCodes.UNDEFINED.name}
