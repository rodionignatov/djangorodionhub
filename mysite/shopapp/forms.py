from django import forms
from .models import Product, Oreder
from django.contrib.auth.models import Group
from django.forms import ModelForm




class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"
    image = forms.ImageField(
#        widget=forms.ClearableFileInput(attrs={"multiple": True}),

    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Oreder
        fields = "user", "delivery_address", "promocode", "products"