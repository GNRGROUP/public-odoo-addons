# Currency Rate Update: Bank of Thailand (BOT)

This odoo module adds Bank of Thailand to currency exchange rates provider. It is required to have THB as your base currency.

## Installation

Odoo version: v14

Include [currency_rate_update](https://github.com/OCA/currency/tree/14.0/currency_rate_update) from OCA into your addons path.

## Configuration

1. Signup and register your application at [BOT API Portal](https://apiportal.bot.or.th/)
2. Goto Setting -> Accounting -> Currencies and update API Key (Client ID) from BOT

## Usage
Goto Accounting -> Configuration -> Currency update services 

There are two ways to update a currency
1. Scheduled update service.
2. Manual update via wizard


**BOT updates exchange rates at 6PM on their working days.**

**Maximum range for the update wizard is 30 days.**

