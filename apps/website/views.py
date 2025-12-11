from django.shortcuts import render
from config import settings

def main(request):
    context = {
        "mapbox_token": settings.MAPBOX_API_KEY,
    }
    return render(request, 'form.html', context=context)