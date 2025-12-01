from django.shortcuts import render
from django.http import HttpResponse

def reservation_test(request):
    return HttpResponse("Hello world!")