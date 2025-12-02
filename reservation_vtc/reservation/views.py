from django.shortcuts import render

def reservation(request):
    data = {
        "address_start": request.POST.get("address_start"),
        "address_stop": request.POST.get("address_stop"),
        "date_start": request.POST.get("date_start"),
        "time_start": request.POST.get("time_start"),
        "car_type": request.POST.get("car_type"),
        "nb_passengers": request.POST.get("nb_passengers"),
        "nb_luggages": request.POST.get("nb_luggages"),
        "trip_type": request.POST.get("trip_type"),
        "last_name": request.POST.get("last_name"),
        "first_name": request.POST.get("first_name"),
        "phone": request.POST.get("phone"),
        "email": request.POST.get("email"),
        "note": request.POST.get("note"),
    }
    return render(request, 'reservation.html', data)