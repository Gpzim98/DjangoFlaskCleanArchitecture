from enum import Enum

class ErrorCodes(Enum):
    CHECKINAFTERCHECKOUT = 'Checkin date cannot be after checkout'
    CUSTOMERISREQUIRED = "Customer is required"
    CUSTOMERSHOULDBEOLDERTHAN18 = 'Customer should be older than 18'
    INVALIDCUSTOMERDOCUMENT = 'Invalid customer document'
    UNDEFINED = 'Undefined'

class SuccessCodes(Enum):
    SUCCESS = 'Success'

class BookingStatuses(Enum):
    OPEN = 0
    RESERVED = 1 
    FINISHED = 2
    CANCELED = 3
