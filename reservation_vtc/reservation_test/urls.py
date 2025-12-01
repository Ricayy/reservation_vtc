from django.urls import path
from . import views

urlpatterns = [
    path('reservation_test/', views.reservation_test, name='reservation_test'),
]
