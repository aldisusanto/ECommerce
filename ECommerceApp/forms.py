from django import forms

from ECommerceApp.models import Merchant


class MerchantForm(forms.Form):
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "off"}))
