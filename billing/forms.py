from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "date", "amount", "note"]
        widgets = {
            "member": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }
