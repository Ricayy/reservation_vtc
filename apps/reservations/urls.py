from django.urls import path
from . import views

urlpatterns = [
    path("validation/", views.validation_reservation, name="validation"),
    path("reservation/<int:id_res>/pdf/", views.preview_order_pdf, name="order"),
]
