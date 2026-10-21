from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "date", "amount", "note"]
        widgets = {
            "member": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "amount": forms.NumberInput(
                attrs={"placeholder": " ", "step": "0.01", "min": "0"}
            ),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }
