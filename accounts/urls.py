# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
   
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("addresses/", views.manage_addresses, name="manage_addresses"),
    
    # NEW: simple password-reset page
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
]

