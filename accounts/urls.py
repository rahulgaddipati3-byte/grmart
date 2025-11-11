# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ---------- AUTH: LOGIN / LOGOUT / SIGNUP ----------

    # Login using Django's built-in auth view + your custom template
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/registration/login.html"
        ),
        name="login",
    ),

    # Logout – send user back to your home page
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="home"   # or "store:product_list" if you prefer
        ),
        name="logout",
    ),

    # Sign-up (this must match views.signup in accounts/views.py)
    path(
        "signup/",
        views.signup,
        name="signup",
    ),

    # ---------- PASSWORD RESET FLOW ----------

    # 1) User submits email
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/registration/password_reset_form.html"
        ),
        name="password_reset",
    ),

    # 2) “We’ve emailed you reset instructions” page
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    # 3) Link from email – page where user sets a new password
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),

    # 4) Password successfully changed
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
