from django import forms

from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["member", "date", "count", "note"]
        widgets = {
            "member": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "count": forms.NumberInput(attrs={"class": "form-control"}),
            "note": forms.TextInput(attrs={"class": "form-control"}),
        }
