from booking_service.domain.booking.entities import Customer

class CustomerDto(object):
    name: str
    age: int
    document: str
    email: str
    id: int

    def __init__(self, name: str, age: int, document: str, email: str) -> None:
        self.name = name
        self.age = age
        self.document = document
        self.email = email
        self.id = None

    def to_domain(self):
        customer = Customer(self.name, self.age, self.document, self.email)
        return customer

    def to_dto(self, customer: Customer):
        return CustomerDto(
            name=customer.name, age=customer.age, document=customer.document, email=customer.email)