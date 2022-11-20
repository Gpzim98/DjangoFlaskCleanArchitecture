from .exceptions import *

class Customer(object):
    name: str
    age: int
    document: str
    email: str

    def __init__(self, name: str, age: int, document: str, email: str) -> None:
        self.name = name
        self.age = age
        self.document = document
        self.email = email

    def is_valid(self):
        if len(self.document) < 5:
            raise InvalidCustomerDocumentException('Invalid document number')
        elif self.age < 18:
            raise CustomerShouldBeOlderThan18('Customer should be older than 18')

        return True