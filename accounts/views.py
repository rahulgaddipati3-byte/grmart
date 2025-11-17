from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def login_view(request):
    """
    Show the login form and authenticate the user.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # If there is ?next=/something/ in the URL, go there after login.
            next_url = request.GET.get("next") or "/"
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    return render(
        request,
        "accounts/registration/login.html",
        {"form": form},
    )


def logout_view(request):
    """
    Log the user out and send them back to home.
    """
    logout(request)
    return redirect("/")  # home page


def signup_view(request):
    """
    Show the registration form and create a new user.
    After successful signup, log the user in and send them to home.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # 🔥 IMPORTANT: no more 'product_list' here
            return redirect("/")  # home page after signup
    else:
        form = UserCreationForm()

    return render(
        request,
        "accounts/registration/signup.html",
        {"form": form},
    )
@login_required
def manage_addresses(request):
    return render(request, "accounts/manage_addresses.html")