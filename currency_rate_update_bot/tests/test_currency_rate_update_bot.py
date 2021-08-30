import datetime
from unittest.mock import patch, Mock
from urllib.error import HTTPError
from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestResCurrencyRateProviderBOT(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env['res.company'].create({'name': 'dummyCorp'})
        self.currency = self.env.ref('base.THB')
        self.provider = self.env['res.currency.rate.provider'].create({
            'company_id': self.company.id,
            'service': 'BOT',
            'currency_ids': [
                (4, self.currency.id),
            ],
        })

    def test_supported_currencies(self):
        supported_currencies = self.provider._get_supported_currencies()
        self.assertEqual(len(supported_currencies), 48)

    def test_bot_get_exchange_rates_raise_exception_when_no_api_key(self):
        self.assertRaises(UserError, self.provider._bot_get_exchange_rates, "")

    @patch('urllib.request.urlopen')
    def test_bot_get_exchange_rates_raise_exception_when_bad_response(self, mocked_urlopen):
        url = "https://dummy"
        mocked_urlopen.side_effect = HTTPError(url, 400, 'bad request', None, None)
        self.company.bot_api_key = "1234"
        self.assertRaises(HTTPError, self.provider._bot_get_exchange_rates, url)

    @patch('urllib.request.urlopen')
    def test_bot_get_exchange_rates(self, mocked_urlopen):
        self.company.bot_api_key = "1234"
        url = "https://dummy"

        mocked_urlopen.return_value.__enter__.return_value = MockResponse('ok')
        response = self.provider._bot_get_exchange_rates(url)
        self.assertEqual(response, 'ok')

    @patch('urllib.request.urlopen')
    def test_obtain_rates(self, mocked_urlopen):
        raw_usd_resp = """
        {
            "result": {
                "timestamp": "2021-08-25 09:14:17",
                "api": "Daily Weighted-average Interbank Exchange Rate - THB / USD",
                "data": {
                    "data_detail": [
                        {
                            "period": "2021-08-24",
                            "currency_id": "USD",
                            "currency_name_th": "สหรัฐอเมริกา : ดอลลาร์ (USD)",
                            "currency_name_eng": "USA : DOLLAR (USD) ",
                            "buying_sight": "32.8801000",
                            "buying_transfer": "32.9768000",
                            "selling": "33.3247000",
                            "mid_rate": "33.1508000"
                        }
                    ]
                }
            }
        }
        """
        raw_eur_resp = """
        {
            "result": {
                "timestamp": "2021-08-25 09:14:17",
                "api": "Daily Weighted-average Interbank Exchange Rate - THB / USD",
                "data": {
                    "data_detail": [
                        {
                            "period": "2021-08-24",
                            "currency_id": "EUR",
                            "currency_name_th": "ยูโรโซน : ยูโร (EUR)",
                            "currency_name_eng": "EURO ZONE : EURO (EUR)",
                            "buying_sight": "38.4150000",
                            "buying_transfer": "38.5251000",
                            "selling": "39.2936000",
                            "mid_rate": "38.9094000"
                        }
                    ]
                }
            }
        }        
        """
        self.company.bot_api_key = "1234"
        url = "https://dummy"

        mocked_urlopen.return_value.__enter__.side_effect = [MockResponse(raw_usd_resp), MockResponse(raw_eur_resp)]
        content = self.provider._obtain_rates("THB", ["USD", "EUR"], datetime.date.today(), datetime.date.today())

        self.assertTrue("2021-08-24" in content)
        self.assertTrue("USD" in content["2021-08-24"])
        self.assertEqual(content["2021-08-24"]["USD"], 1.0/33.1508000)
        self.assertEqual(content["2021-08-24"]["EUR"], 1.0/38.9094000)

    def test_obtain_rates_raise_exception_when_not_THB_base(self):
        self.assertRaises(UserError, self.provider._obtain_rates, "USD",
                          "EUR", datetime.date.today(), datetime.date.today())

    def test_obtain_rates_raise_exception_when_date_range_is_more_than_31_days(self):
        self.assertRaises(UserError, self.provider._obtain_rates, "USD",
                          "EUR", datetime.date.today() - datetime.timedelta(days=31), datetime.date.today())


class MockResponse(object):

    def __init__(self, resp_data):
        self.resp_data = resp_data

    def read(self):
        return self.resp_data
