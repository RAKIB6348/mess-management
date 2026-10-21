from django import forms

from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ["member", "date", "count", "note"]
        widgets = {
            "member": forms.Select(),
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "text",
                    "placeholder": " ",
                    "onfocus": "(this.type='date')",
                    "onblur": "if(!this.value) this.type='text'",
                },
            ),
            "count": forms.NumberInput(
                attrs={"placeholder": " ", "min": 1}
            ),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Blank empty option so the select looks empty (like the date field).
        self.fields["member"].empty_label = " "
