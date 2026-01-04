from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'payment_mode', 'description', 'receipt_image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional details...'}),
            'receipt_image': forms.FileInput(attrs={'class': 'form-control'}),
        }