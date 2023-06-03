import json
import pathlib

import responses

from .exchange_provider import (
    MonoExchange,
    PrivatExchange,
    OschadExchange,
    CurrencyExchange,
    VkurseExchange,
    MinfinExchange,
)

root = pathlib.Path(__file__).parent

# Create your tests here.


@responses.activate
def test_exchange_mono():
    mocked_response = json.load(open(root / "fixtures/mono_response.json"))
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406

@responses.activate
def test_privat_rate():
    mocked_response = json.load(open(root / "fixtures/privat_response.json"))
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.45318

@responses.activate
def test_oschad_rate():
    mocked_response = json.load(open(root / "fixtures/oschad_response.json"))
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=mocked_response,
    )
    e = OschadExchange("oschad", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686

@responses.activate
def test_currency_rate():
    mocked_response = json.load(open(root / "fixtures/currency_response.json"))
    responses.get(
        "https://api.currencyapi.com/v3/"
        "latest?apikey=Qja2YHvZFI5TI4eZdu24l1etllOPAnQ1mxlhlI2a&currencies=EUR%2CUSD&base_currency=UAH",
        json=mocked_response,
    )
    e = CurrencyExchange("currency", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == float(1 / 0.027082)

@responses.activate
def test_vkurse_rate():
    mocked_response = json.load(open(root / "fixtures/vkurse_response.json"))
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.50

@responses.activate
def test_minfin_rate():
    mocked_response = json.load(open(root / "fixtures/minfin_response.json"))
    responses.get(
        "https://api.minfin.com.ua/summary/05012c3dcf6783803a3b6a3967a72af9fc58beb9/",
        json=mocked_response,
    )
    e = MinfinExchange("minfin", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.65
