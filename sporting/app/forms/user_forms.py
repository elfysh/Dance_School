from django import forms


class FilterForm(forms.Form):
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "card__input",
            "type": "date"
        })
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            "class": "card__input",
            "type": "date"
        })
    )
    styles = forms.MultipleChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "card__input"
        }),
        choices=[]
    )

    def update_choices(self, choices):
        self.fields['styles'].choices = choices

