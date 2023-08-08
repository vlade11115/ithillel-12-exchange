from django import forms


class ExchangeForm(forms.Form):
    choose_operation = (
        ("sell", "Buy"),
        ("buy", "Sell"),
    )
    choose_currency = (
        ("USD", "USD"),
        ("EUR", "EUR"),
    )

    operation = forms.ChoiceField(
        choices=choose_operation,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
    currency_value = forms.IntegerField(max_value=1000000)
    currency = forms.ChoiceField(
        choices=choose_currency,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
