from django import forms


class MasterClassForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Название мастер класса",
            "class": "card__input"
        })
    )

    hall = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    choreographer = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
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

    time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={
            "class": "card__input",
            "type": "time"
        }
        )
    )

    def update_choices(self, halls, choreographers):
        self.fields['hall'].choices = halls
        self.fields['choreographer'].choices = choreographers


class EditMasterClassForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Название мастер класса",
            "class": "card__input"
        })
    )

    hall = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    choreographer = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
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

    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={
            "class": "card__input",
            "type": "time"
        }
        )
    )

    def update_choices(self, halls, choreographers):
        self.fields['hall'].choices = halls
        self.fields['choreographer'].choices = choreographers
