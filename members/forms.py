from django import forms

from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "phone", "email", "status", "note"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": " "}),
            "phone": forms.TextInput(attrs={"placeholder": " "}),
            "email": forms.EmailInput(attrs={"placeholder": " "}),
            "status": forms.Select(),
            "note": forms.Textarea(attrs={"placeholder": " ", "rows": 3}),
        }
