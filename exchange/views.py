import datetime
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Min
from django.http import HttpResponse
from django.shortcuts import render

from exchange.forms import CounterForm
from .models import Counter
from .models import Rate
from .tasks import start_exchange


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


# Create your views here.


def index(request):
    if request.method == "GET":
        start_exchange.delay("mono", "USD", "UAH")
        start_exchange.delay("privat", "USD", "UAH")
        start_exchange.delay("vkurse", "USD", "UAH")
        start_exchange.delay("nbu", "USD", "UAH")
        start_exchange.delay("minfin", "USD", "UAH")
        start_exchange.delay("mono", "EUR", "UAH")
        start_exchange.delay("privat", "EUR", "UAH")
        start_exchange.delay("vkurse", "EUR", "UAH")
        start_exchange.delay("nbu", "EUR", "UAH")
        start_exchange.delay("minfin", "EUR", "UAH")
        current_date = datetime.date.today()
        current_ratesUs = Rate.objects.filter(date=current_date, currency_a='USD').all().values().aggregate(Min('sell'))
        current_ratesUb = Rate.objects.filter(date=current_date, currency_a='USD').all().values().aggregate(Min('buy'))
        current_ratesEs = Rate.objects.filter(date=current_date, currency_a='EUR').all().values().aggregate(Min('sell'))
        current_ratesEb = Rate.objects.filter(date=current_date, currency_a='EUR').all().values().aggregate(Min('buy'))
        print(current_ratesUb)
        currUS = float(current_ratesUs['sell__min'])
        currUB = float(current_ratesUb['buy__min'])
        currES = float(current_ratesEs['sell__min'])
        currEB = float(current_ratesEb['buy__min'])
        form = CounterForm()
        context = {"form": form, 'message1': str(currUS) + ' Put this full name of currency> USD-sell ',
                   'message2': str(currUB) + ' Put this full name of currency> USD-buy ',
                   'message3': str(currES) + ' Put this full name of currency> EUR-sell ',
                   'message4': str(currEB) + ' Put this full name of currency> EUR-buy '}
        return render(request, "counter.html", context)
    elif request.method == "POST":
        form = CounterForm(request.POST)
        if form.is_valid():
            form.save()
            count = Counter.objects.latest('id').counter
            which = Counter.objects.latest('id').chois
            current_date = datetime.date.today()
            current_ratesUs = Rate.objects.filter(date=current_date, currency_a='USD').all().values().aggregate(
                Min('sell'))
            current_ratesUb = Rate.objects.filter(date=current_date, currency_a='USD').all().values().aggregate(
                Min('buy'))
            current_ratesEs = Rate.objects.filter(date=current_date, currency_a='EUR').all().values().aggregate(
                Min('sell'))
            current_ratesEb = Rate.objects.filter(date=current_date, currency_a='EUR').all().values().aggregate(
                Min('buy'))
            print(current_ratesUb)
            currUS = float(current_ratesUs['sell__min'])
            currUB = float(current_ratesUb['buy__min'])
            currES = float(current_ratesEs['sell__min'])
            currEB = float(current_ratesEb['buy__min'])
            if which == "USD-sell":
                res1 = currUS * count
                return HttpResponse(str(res1) + ' USD')
            if which == "USD-buy":
                res2 = currUB * count
                return HttpResponse(str(res2) + ' USD')
            if which == "EUR-sell":
                res2 = currES * count
                return HttpResponse(str(res2) + ' EUR')
            if which == "EUR-buy":
                res2 = currEB * count
                return HttpResponse(str(res2) + ' EUR')
