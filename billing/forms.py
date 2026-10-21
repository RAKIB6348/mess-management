from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "date", "amount", "note"]
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
            "amount": forms.NumberInput(
                attrs={"placeholder": " ", "step": "0.01", "min": "0"}
            ),
            "note": forms.TextInput(attrs={"placeholder": " "}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Blank empty option so the select looks empty (like the date field).
        self.fields["member"].empty_label = " "
