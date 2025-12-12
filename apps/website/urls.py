from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationCreateView.as_view(), name='reservation_add'),
    path('confirm_reservation/', views.confirm_reservation, name='confirm_reservation'),
]