from django import forms


class ChoreographerForm(forms.Form):
    choreographer_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Имя хореографа",
            "class": "card__input"
        })
    )
    style = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    def update_choices(self, choices):
        self.fields['style'].choices = choices


class EditChoreographerForm(forms.Form):
    choreographer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Имя хореографа",
            "class": "card__input"
        })
    )
    style = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            "class": "card__input"
        })
    )

    def update_choices(self, choices):
        self.fields['style'].choices = choices
