# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def signup(request):
    """User registration view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # After signup go to product list
            return redirect("store:product_list")
    else:
        form = UserCreationForm()

    return render(request, "accounts/registration/signup.html", {"form": form})


def login_view(request):
    """User login view."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # After login go to product list
            return redirect("store:product_list")
    else:
        form = AuthenticationForm(request)

    return render(request, "accounts/registration/login.html", {"form": form})


@login_required
def logout_view(request):
    """User logout view."""
    logout(request)
    # After logout go back to products list (or home)
    return redirect("store:product_list")
