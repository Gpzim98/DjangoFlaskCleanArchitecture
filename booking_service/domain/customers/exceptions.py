class CustomerShouldBeOlderThan18(Exception):
    def __init__(self, message):
        self.message = message

class InvalidCustomerDocumentException(Exception):
    def __init__(self, message):
        self.message = message
