from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = [
            "full_name", "email", "phone",
            "address1", "address2", "city", "state", "postcode",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email":     forms.EmailInput(attrs={"class": "form-control"}),
            "phone":     forms.TextInput(attrs={"class": "form-control"}),

            "address1":  forms.TextInput(attrs={"class": "form-control"}),
            "address2":  forms.TextInput(attrs={"class": "form-control"}),
            "city":      forms.TextInput(attrs={"class": "form-control"}),
            "state":     forms.TextInput(attrs={"class": "form-control"}),
            "postcode":  forms.TextInput(attrs={"class": "form-control"}),
        }
