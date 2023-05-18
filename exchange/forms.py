from django import forms


class ExchangeForm(forms.Form):
    OPERATION = (
        ("sell", "Купити"),
        ("buy", "Продати"),
    )
    CURRENCY = (
        ("USD", "USD"),
        ("EUR", "EUR"),
    )

    operation = forms.ChoiceField(
        choices=OPERATION,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    currency_value = forms.IntegerField(
        max_value=1000000,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "width: 30%"}
        ),
    )
    currency = forms.ChoiceField(
        choices=CURRENCY,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
