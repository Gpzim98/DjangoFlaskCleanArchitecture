class CheckinDateCannotBeAfterCheckoutDate(Exception):
    def __init__(self, message):
        self.message = message

class CustomerCannotBeBlank(Exception):
    def __init__(self, message):
        self.message = message

class BookingUpdateRequiresExistingBookingId(Exception):
    def __init__(self, message):
        self.message = message

class BookingWithThisStatusCannotBeDeleted(Exception):
    def __init__(self, message):
        self.message = message
