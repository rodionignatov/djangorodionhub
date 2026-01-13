from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    # Вариант 1: Без multiple
    images = forms.ImageField(
        widget=forms.FileInput(),  # ← Просто FileInput без attrs
        required=False,
    )

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()