from django import forms


class EventForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Название ивента",
            "class": "card__input"
        })
    )

    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "class": "card__input",
            "type": "date"
        })
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Описание ивента",
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

    def update_choices(self, choices):
        self.fields['dance_school'].choices = choices


class EditEventForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Название ивента",
            "class": "card__input"
        })
    )

    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "card__input",
            "type": "date"
        })
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Описание ивента",
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

    def update_choices(self, choices):
        self.fields['dance_school'].choices = choices
