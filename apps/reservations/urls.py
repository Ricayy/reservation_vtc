from django.urls import path
from . import views

urlpatterns = [
    path('validation/', views.validation_reservation, name='validation'),
]