from enum import Enum

class ErrorCodes(Enum):
    CHECKINAFTERCHECKOUT = 'Checkin date cannot be after checkout'
    CUSTOMERISREQUIRED = "Customer is required"
    UNDEFINED = 'Undefined'