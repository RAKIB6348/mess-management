from django import forms

from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["member", "date", "count", "note"]
        widgets = {
            "member": forms.Select(),
            "date": forms.DateInput(
                attrs={"type": "date", "class": "flat"}
            ),
            "count": forms.NumberInput(
                attrs={"class": "flat", "min": 1}
            ),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }
