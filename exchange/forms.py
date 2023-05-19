from django import forms

from exchange.models import Counter


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = ["counter", "chois"]
