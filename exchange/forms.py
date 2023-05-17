from django import forms


class ExchangeForm(forms.Form):
    OPERATION = (
        ("sell", "Sell"),
        ("buy", "Buy"),
    )
    CURRENCY = (
        ("USD", "USD"),
        ("EUR", "EUR"),
    )

    operation = forms.ChoiceField(choices=OPERATION)
    currency_value = forms.IntegerField(max_value=1000000)
    currency = forms.ChoiceField(choices=CURRENCY)
