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

    def get_booking_by_id(self, booking_id: int, user_dto: UserDto):
        booking = self.storage.get_booking_by_id(booking_id)
        if booking.status == BookingStatuses.CANCELED.name and not user_dto.is_admin:
            return {'message': ErrorCodes.USERNOTALLOWEDTOACCESSDATA.value, 'code': ErrorCodes.USERNOTALLOWEDTOACCESSDATA.name}
        else:
            return {'message': SuccessCodes.SUCCESS.value, 'data': booking, 'code': SuccessCodes.SUCCESS.name}

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

    def update_booking(self, booking_dto: BookingDto):
        booking_aggregate = booking_dto.to_domain()
        try:
            booking_aggregate.update_booking()
            final_dto = booking_dto.to_dto(booking_aggregate)
            self.storage.update_booking(final_dto)
            return {'message': SuccessCodes.SUCCESS.value, 'code': SuccessCodes.SUCCESS.name}
        except CheckinDateCannotBeAfterCheckoutDate as e:
            return {'message': ErrorCodes.CHECKINAFTERCHECKOUT.value, 'code': ErrorCodes.CHECKINAFTERCHECKOUT.name}
        except CustomerCannotBeBlank as e:
            return {'message': ErrorCodes.CUSTOMERISREQUIRED.value, 'code': ErrorCodes.CUSTOMERISREQUIRED.name}
        except CustomerShouldBeOlderThan18 as e:
            return {'message': ErrorCodes.CUSTOMERSHOULDBEOLDERTHAN18.value, 'code': ErrorCodes.CUSTOMERSHOULDBEOLDERTHAN18.name}
        except InvalidCustomerDocumentException as e:
            return {'message': ErrorCodes.INVALIDCUSTOMERDOCUMENT.value, 'code': ErrorCodes.INVALIDCUSTOMERDOCUMENT.name}
        except BookingUpdateRequiresExistingBookingId as e:
            return {'message': ErrorCodes.UPDATEBOOKINGREQUIRESBOOKINGID.value, 'code': ErrorCodes.UPDATEBOOKINGREQUIRESBOOKINGID.name}
        except Exception as e:
            return {'message': ErrorCodes.UNDEFINED.value, 'code': ErrorCodes.UNDEFINED.name}

    def delete_booking(self, booking_id: int):
        try:
            booking = self.storage.get_booking_by_id(booking_id)
            domain_aggregate = booking.to_domain()
            domain_aggregate.delete_booking()
            final_dto = booking.to_dto(domain_aggregate)
            self.storage.delete_booking(final_dto)
            return {'message': SuccessCodes.SUCCESS.value, 'code': SuccessCodes.SUCCESS.name}
        except BookingWithThisStatusCannotBeDeleted as e:
            return {'message': ErrorCodes.BOOKINGSTATUSDOESNOTALLOWDELETE.value, 'code': ErrorCodes.BOOKINGSTATUSDOESNOTALLOWDELETE.name}
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
