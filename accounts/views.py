# accounts/views.py
import random
import time

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
# --- Password reset with OTP ---

def password_reset_request(request):
    """
    Step 1: user enters email, we send a 6-digit OTP and store it in the session.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect("accounts:password_reset_request")

        # Generate 6-digit OTP
        otp = random.randint(100000, 999999)
        # store in session with 10-minute expiry
        request.session["pw_reset"] = {
            "user_id": user.id,
            "otp": str(otp),
            "expires_at": int(time.time()) + 600,  # now + 10 min
        }

        # send email
        subject = "G.R Mart password reset code"
        message = f"Hello {user.username},\n\nYour G.R Mart password reset code is: {otp}\nThis code is valid for 10 minutes."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        messages.success(request, "We’ve sent an OTP to your email (valid 10 minutes).")
        return redirect("accounts:password_reset_otp")

    return render(request, "accounts/password_reset_request.html")


def password_reset_otp(request):
    """
    Step 2: user enters OTP + new password, we verify and change password.
    """
    data = request.session.get("pw_reset")
    if not data:
        messages.error(request, "Password reset session expired. Please try again.")
        return redirect("accounts:password_reset_request")

    # expiry check
    if int(time.time()) > data.get("expires_at", 0):
        request.session.pop("pw_reset", None)
        messages.error(request, "Your OTP has expired. Please request a new one.")
        return redirect("accounts:password_reset_request")

    if request.method == "POST":
        otp_input = request.POST.get("otp", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if otp_input != data.get("otp"):
            messages.error(request, "Invalid OTP.")
            return redirect("accounts:password_reset_otp")

        if not password1 or password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:password_reset_otp")

        try:
            user = User.objects.get(id=data["user_id"])
        except User.DoesNotExist:
            request.session.pop("pw_reset", None)
            messages.error(request, "User not found. Please try again.")
            return redirect("accounts:password_reset_request")

        # Set new password
        user.set_password(password1)
        user.save()

        # Clean session
        request.session.pop("pw_reset", None)

        messages.success(request, "Password reset successfully. Please log in.")
        return redirect("accounts:login")

    return render(request, "accounts/password_reset_otp.html")

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# … your existing imports and views …

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {
        "user": request.user,
    })
# accounts/views.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

def signup(request):
    """
    Very simple registration view using Django's built-in UserCreationForm.
    Renders accounts/registration/signup.html
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account was created successfully.")
            auth_login(request, user)          # log the user in
            return redirect("home")            # or "store:product_list"
    else:
        form = UserCreationForm()

    return render(request, "accounts/registration/signup.html", {"form": form})
