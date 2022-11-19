from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('booking/', include('booking.urls')),
    path('admin/', admin.site.urls),
]
