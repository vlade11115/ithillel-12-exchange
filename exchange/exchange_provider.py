import abc
import dataclasses
import enum

import requests


class ExchangeCodes(enum.Enum):
    USD = 840
    EUR = 978
    UAH = 980


@dataclasses.dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class ExchangeBase(abc.ABC):
    """
    Base class for exchange providers, should define get_rate() method
    """

    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair: SellBuy = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()
        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])

                return


class PrivatExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["ccy"] == self.currency_a and rate["base_ccy"] == self.currency_b:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class OschadExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["cc"] == self.currency_a and self.currency_b == "UAH":
                self.pair = SellBuy(float(rate["rate"]), float(rate["rate"]))


class CurrencyExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.currencyapi.com/v3/latest?apikey=Qja2YHvZFI5TI4eZdu24l1etllOPAnQ1mxlhlI2a&currencies=EUR%2CUSD&base_currency=UAH"
        )
        r.raise_for_status()
        if self.currency_b == "UAH":
            rate = r.json()["data"][self.currency_a]
            self.pair = SellBuy(float(1 / rate["value"]), float(1 / rate["value"]))


class VkurseExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get("https://vkurse.dp.ua/course.json")
        r.raise_for_status()
        if self.currency_b == "UAH":
            if self.currency_a == "USD":
                rate = r.json()["Dollar"]
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))
            elif self.currency_a == "EUR":
                rate = r.json()["Euro"]
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class MinfinExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.minfin.com.ua/summary/05012c3dcf6783803a3b6a3967a72af9fc58beb9/"
        )
        r.raise_for_status()
        if self.currency_a == "USD" and self.currency_b == "UAH":
            rate = r.json()["usd"]
            self.pair = SellBuy(float(rate["ask"]), float(rate["bid"]))
        elif self.currency_a == "EUR" and self.currency_b == "UAH":
            rate = r.json()["eur"]
            self.pair = SellBuy(float(rate["ask"]), float(rate["bid"]))
