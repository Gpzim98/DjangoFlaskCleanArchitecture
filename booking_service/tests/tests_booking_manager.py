import unittest
from datetime import datetime, timedelta
import sys
sys.path.append('..')
sys.path.append('../..')
from domain.booking.exceptions import *
from domain.customers.exceptions import *
from application.booking.booking_manager import BookingManager
from application.booking.booking_dto import BookingDto
from application.customers.customer_dto import CustomerDto

class BookingAggregateManagerTests(unittest.TestCase):

    def test_checkin_date_cannot_be_after_checkout(self):
        checkin = datetime.today()
        checkout = datetime.today() - timedelta(days=1)
        customer = CustomerDto("Customer", 18, "doc123", "a@a.com")
        booking_dto = BookingDto(checkin=checkin, checkout=checkout, customer=customer)
        manager = BookingManager()
        res = manager.create_new_booking(booking_dto)
        self.assertEqual(res['code'], 'CHECKINAFTERCHECKOUT')

    def test_customer_should_be_older_than_18(self):
        checkin = datetime.today()
        checkout = datetime.today()
        customer = CustomerDto("Customer", 17, "doc123", "a@a.com")
        booking_dto = BookingDto(checkin=checkin, checkout=checkout, customer=customer)
        manager = BookingManager()
        res = manager.create_new_booking(booking_dto)
        self.assertEqual(res['code'], 'CUSTOMERSHOULDBEOLDERTHAN18')

    def test_customer_document_should_be_valid(self):
        checkin = datetime.today()
        checkout = datetime.today()
        customer = CustomerDto("Customer", 18, "doc1", "a@a.com")
        booking_dto = BookingDto(checkin=checkin, checkout=checkout, customer=customer)
        manager = BookingManager()
        res = manager.create_new_booking(booking_dto)
        self.assertEqual(res['code'], 'INVALIDCUSTOMERDOCUMENT')

    def test_create(self):
        checkin = datetime.utcnow()
        checkout = datetime.today()
        customer = CustomerDto("Customer", 18, "doc123", "a@a.com")
        booking_dto = BookingDto(checkin=checkin, checkout=checkout, customer=customer)
        manager = BookingManager()
        res = manager.create_new_booking(booking_dto)
        self.assertEqual(res['code'], 'SUCCESS')

if __name__ == '__main__':
    unittest.main()
