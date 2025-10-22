from django import forms
from .models import Producto

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['imagen','title', 'description', 'important', 'price',]
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }