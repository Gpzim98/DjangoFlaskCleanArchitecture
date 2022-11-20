from django.urls import path
from .views import home, create_new

urlpatterns = [
    path('create-new', create_new),
    path('', home),
]
