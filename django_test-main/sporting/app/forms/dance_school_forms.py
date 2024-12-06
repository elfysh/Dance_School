from django import forms


class DanceSchoolForm(forms.Form):
    # Fields: name, address, phone
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Название школы",
            "class": "card__input"
        })
    )
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Адрес",
            "class": "card__input"
        })
    )
    # Phone number: +{code} 123 456 78 90
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "+7 123 456 78 90",
            "class": "card__input"
        })
    )


class EditDanceSchoolForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Название школы",
            "class": "card__input"
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Адрес",
            "class": "card__input"
        })
    )
    # Phone number: +{code} 123 456 78 90
    phone = forms.CharField(
        required=False,
        help_text="Format: +{code} 123 456 78 90",
        widget=forms.TextInput(attrs={
            "placeholder": "+7 123 456 78 90",
            "class": "card__input"
        })
    )
