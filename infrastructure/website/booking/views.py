from django.shortcuts import HttpResponse, render
from datetime import datetime
from booking_service.application.booking.booking_manager import BookingManager
from booking_service.application.booking.booking_dto import *
from booking_service.application.customers.customer_dto import CustomerDto
from .repositories import BookingRepository
from django.shortcuts import redirect

def home(request):
    user_dto = UserDto(request.user.first_name, request.user.is_superuser)
    user_dto.id = request.user.id
    repository = BookingRepository()
    manager = BookingManager(repository)
    bookings = manager.get_bookings(user_dto)
    return render(request, 'index.html', {'bookings': bookings})

def create_new(request):
    checkin = datetime.strptime(request.POST.get('checkin'),  "%Y-%m-%dT%H:%M")
    checkout = datetime.strptime(request.POST.get('checkout'),"%Y-%m-%dT%H:%M")

    customer_dto = get_customer_from_request(request)

    dto = BookingDto(checkin, checkout, customer_dto)
    repository = BookingRepository()
    manager = BookingManager(repository)
    res = manager.create_new_booking(dto)

    if res['code'] != 'SUCCESS':
        return render(request, 'index.html', {'res': res})
    else:
        return render(request, 'confirmation.html')


def update(request, id):
    user_dto = UserDto(request.user.first_name, request.user.is_superuser)
    repository = BookingRepository()
    manager = BookingManager(repository)

    if request.method == 'GET':
        resp = manager.get_booking_by_id(id, user_dto)
        if resp['code'] == 'SUCCESS':
            resp['checkin']  = resp['data'].checkin.strftime("%Y-%m-%dT%H:%M")
            resp['checkout'] = resp['data'].checkout.strftime("%Y-%m-%dT%H:%M")
            return render(request, 'update.html', resp)
        else:
            return render(request, 'index.html', {'res': resp['message']})
    elif request.method == 'POST':
        checkin = datetime.strptime(request.POST.get('checkin'),  "%Y-%m-%dT%H:%M")
        checkout = datetime.strptime(request.POST.get('checkout'),"%Y-%m-%dT%H:%M")

        customer_dto = get_customer_from_request(request)
        dto = BookingDto(checkin, checkout, customer_dto)
        dto.id = id
        repository = BookingRepository()
        manager = BookingManager(repository)
        res = manager.update_booking(dto)

        if res['code'] != 'SUCCESS':
            return render(request, 'index.html', {'res': res})
        else:
            return render(request, 'confirmation.html')

def delete(request, id):
    repository = BookingRepository()
    manager = BookingManager(repository)
    res = manager.delete_booking(id)
    if res['code'] == 'SUCCESS':
        return render(request, 'delete_confirmation.html')
    else:
        return HttpResponse(res['message'])

def get_customer_from_request(request):
    name = request.POST.get('name')
    age = int(request.POST.get('age'))
    document = request.POST.get('document')
    email = request.POST.get('email')
    customer_dto = CustomerDto(name, age, document, email)
    return customer_dto
