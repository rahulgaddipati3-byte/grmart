from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_GET

@require_GET
def logout_get(request):
    logout(request)
    return redirect('/')
# shop/views.py
from django.views.generic import TemplateView



   
from django.shortcuts import render

def home(request):
    return render(request, "shop/home.html")
