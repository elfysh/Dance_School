from django import forms


class HallForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Название зала",
            "class": "card__input"
        })
    )

    dance_school = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    capacity = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "placeholder": "Вместимость зала",
            "class": "card__input"
        })
    )

    def update_choices(self, choices):
        self.fields['dance_school'].choices = choices


class EditHallForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Название зала",
            "class": "card__input"
        })
    )

    dance_school = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    capacity = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            "placeholder": "Вместимость зала",
            "class": "card__input"
        })
    )

    def update_choices(self, choices):
        self.fields['dance_school'].choices = choices
