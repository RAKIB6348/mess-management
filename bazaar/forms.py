from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "title", "amount", "paid_by", "note"]
        widgets = {
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "text",
                    "placeholder": " ",
                    "onfocus": "(this.type='date')",
                    "onblur": "if(!this.value) this.type='text'",
                },
            ),
            "title": forms.TextInput(attrs={"placeholder": " "}),
            "amount": forms.NumberInput(
                attrs={"placeholder": " ", "step": "0.01", "min": "0"}
            ),
            "paid_by": forms.Select(),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }
