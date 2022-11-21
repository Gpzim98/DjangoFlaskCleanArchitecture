from booking_service.domain.booking.exceptions import *
from booking_service.domain.customers.exceptions import *
from .booking_dto import BookingDto, UserDto
from booking_service.domain.booking.enums import *
from .booking_storage import BookingStorage

class BookingManager(object):
    storage: BookingStorage

    def __init__(self, storage: BookingStorage) -> None:
        self.storage = storage

    def get_bookings(self, user_dto: UserDto):
        if user_dto.is_admin:
            return self.storage.get_all_bookings()
        else:
            return self.storage.get_filtered_bookings()

    def create_new_booking(self, booking_dto: BookingDto):
        booking_aggregate = booking_dto.to_domain()

        try:
            booking_aggregate.create_booking()
            final_dto = booking_dto.to_dto(booking_aggregate)
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
