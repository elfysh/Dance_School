from django import forms


class StyleForm(forms.Form):
    style_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "card__input",
            "placeholder": "Название направления"
        })
    )
