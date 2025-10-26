from django import forms
from .models import Producto

class ProductForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['imagen','title', 'description', 'price']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': 1}),
        }