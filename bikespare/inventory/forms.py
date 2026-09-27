from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["name", "phone", "brand", "model", "part", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Full name",
                "required": True,
                "maxlength": 120,
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "Your phone number",
                "required": True,
                "maxlength": 25,
            }),
            "brand": forms.TextInput(attrs={"placeholder": "e.g. Honda"}),
            "model": forms.TextInput(attrs={"placeholder": "e.g. Activa"}),
            "part": forms.TextInput(attrs={
                "placeholder": "Part name or part number",
                "required": True,
                "maxlength": 200,
            }),
            "message": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Model year, quantity or any fitment details",
                "maxlength": 3000,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["phone"].required = True
        self.fields["part"].required = True