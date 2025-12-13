from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.core.models import OdooContactModel
from apps.core.odoo_client import search_read_reservations_by_user
from apps.website.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("reservation_add")
            else:
                error = "Email ou mot de passe incorrect"
    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form, "error": error}
    )


def logout_view(request):
    logout(request)
    return redirect("reservation_add")


@login_required
def profile_view(request):
    reservations = search_read_reservations_by_user(str(request.user))
    print("reservations--------------")
    print(reservations)
    print(reservations["result"][0][OdooContactModel.reservation_id])
    return render(request, "accounts/profile.html", context={"reservations_list": reservations})