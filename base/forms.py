
from django import forms
from .models import Product, Category


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['owner']

    
