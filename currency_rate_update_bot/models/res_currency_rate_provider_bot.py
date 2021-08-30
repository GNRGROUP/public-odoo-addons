import json
import urllib.request

from collections import defaultdict
from datetime import timedelta
from odoo import models, fields
from odoo.exceptions import UserError


class ResCurrencyRateProviderBOT(models.Model):
    _inherit = 'res.currency.rate.provider'

    service = fields.Selection(
        selection_add=[('BOT', 'Bank of Thailand')],
        ondelete={"BOT": "set default"},
    )

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != 'BOT':
            return super()._get_supported_currencies()  # pragma: no cover
        # Retrieved from DAILY_AVG_EXG_RATE API without any currency specified
        return ['AED', 'AUD', 'BDT', 'BHD', 'BND', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EGP', 'EUR',
                'GBP', 'HKD', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'JOD', 'JPY', 'KES', 'KHR', 'KRW',
                'KWD', 'LAK', 'LKR', 'MMK', 'MVR', 'MXN', 'MYR', 'NOK', 'NPR', 'NZD', 'OMR', 'PGK',
                'PHP', 'PKR', 'PLN', 'QAR', 'RUB', 'SAR', 'SEK', 'SGD', 'TWD', 'USD', 'VND', 'ZAR']

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != 'BOT':
            return super()._obtain_rates(base_currency, currencies, date_from,
                                         date_to)  # pragma: no cover

        content = defaultdict(dict)
        if (date_to - timedelta(days=31)) > date_from:
            raise UserError(_('Exceed limit period. Limit period from Bank of Thailand API is 31 days'))

        if base_currency != 'THB':
            raise UserError(_('Only THB base currency is supported with Bank of Thailand!'))

        for currency in currencies:
            url = "https://apigw1.bot.or.th/bot/public/Stat-ExchangeRate/v2/DAILY_AVG_EXG_RATE/?start_period={}&end_period={}&currency={}".format(
                date_from, date_to, currency)
            data = json.loads(self._bot_get_exchange_rates(url))
            rates = data["result"]["data"]["data_detail"]
            for rate in rates:
                if rate["period"]:
                    content[rate["period"]][currency] = 1.0/float(rate[self.company_id.bot_rate_type or "mid_rate"])

        return content

    def _bot_get_exchange_rates(self, url):
        self.ensure_one()
        if not self.company_id.bot_api_key:
            raise UserError(_('No Bank of Thailand API Key specified!'))

        request = urllib.request.Request(url)
        request.add_header('X-IBM-Client-Id', self.company_id.bot_api_key)
        request.add_header('accept', 'application/json')
        with urllib.request.urlopen(request) as response:
            content = response.read()
        return content
