from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 
              'postal_code', 'city', 'email']