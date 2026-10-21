from django import forms

from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["member", "date", "count", "note"]
        widgets = {
            "member": forms.Select(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "count": forms.NumberInput(
                attrs={"placeholder": " ", "min": 1}
            ),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }
