from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "title", "amount", "paid_by", "note"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "flat"}
            ),
            "title": forms.TextInput(attrs={"placeholder": " "}),
            "amount": forms.NumberInput(
                attrs={"class": "flat", "step": "0.01", "min": "0"}
            ),
            "paid_by": forms.Select(),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }
