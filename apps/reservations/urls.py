from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation, name='form'),
    path('validation/', views.validation, name='validation'),
]