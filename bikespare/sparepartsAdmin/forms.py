from django import forms

from inventory.models import Brand, Category, Enquiry, Part


INPUT_CLASS = (
    "w-full bg-slate-50 border border-stone-800 rounded-xl "
    "px-4 py-3 text-sm text-stone-900 placeholder-stone-600 "
    "focus:outline-none focus:border-amber-500 focus:ring-1 "
    "focus:ring-amber-500 transition"
)

TEXTAREA_CLASS = (
    "w-full bg-slate-50 border border-stone-800 rounded-xl "
    "px-4 py-3 text-sm text-stone-100 placeholder-stone-600 "
    "focus:outline-none focus:border-amber-500 focus:ring-1 "
    "focus:ring-amber-500 transition resize-none"
)

SELECT_CLASS = (
    "w-full bg-slate-50 border border-stone-800 rounded-xl "
    "px-4 py-3 text-sm text-stone-900 "
    "focus:outline-none focus:border-amber-500 focus:ring-1 "
    "focus:ring-amber-500 transition"
)


class PartForm(forms.ModelForm):

    class Meta:
        model = Part

        fields = [
            "part_number",
            "name",
            "brand",
            "category",
            "description",
            "compatible_with",
            "quantity",
            "price",
            "is_featured",
            "is_active",
        ]

        widgets = {
            "part_number": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. BP-1001",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. Front Brake Pad",
                }
            ),

            "brand": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": SELECT_CLASS,
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                    "placeholder": "Describe the spare part...",
                }
            ),

            "compatible_with": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. Honda Activa / Yamaha FZ",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASS,
                    "min": 0,
                    "placeholder": "0",
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASS,
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),

            "is_featured": forms.CheckboxInput(
                attrs={
                    "class": (
                        "w-5 h-5 rounded border-stone-700 "
                        "bg-[#181412] text-amber-500 "
                        "focus:ring-amber-500"
                    )
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": (
                        "w-5 h-5 rounded border-stone-700 "
                        "bg-[#181412] text-amber-500 "
                        "focus:ring-amber-500"
                    )
                }
            ),
        }


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand

        fields = [
            "name",
            "slug",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. Honda",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. honda",
                }
            ),
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
            "slug",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. Brake System",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "e.g. brake-system",
                }
            ),
        }


class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry

        fields = [
            "name",
            "phone",
            "brand",
            "model",
            "part",
            "message",
            "is_handled",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                }
            ),

            "brand": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                }
            ),

            "model": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                }
            ),

            "part": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                }
            ),

            "is_handled": forms.CheckboxInput(
                attrs={
                    "class": (
                        "w-5 h-5 rounded border-stone-700 "
                        "bg-[#181412] text-amber-500 "
                        "focus:ring-amber-500"
                    )
                }
            ),
        }