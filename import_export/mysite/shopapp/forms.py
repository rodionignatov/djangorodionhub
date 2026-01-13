from django import forms

# from import_export.mysite.shopapp.models import Product
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
#        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        widget=forms.ClearableFileInput(attrs={"": True}),

    )

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class OrderImportForm(forms.Form):
    file = forms.FileField()















