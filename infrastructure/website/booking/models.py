from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    document = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Booking(models.Model):
    checkin = models.DateField(auto_now=False)
    checkout = models.DateField(auto_now=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Booking for: " + self.customer.name
