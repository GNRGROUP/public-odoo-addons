# Copyright 2021 G.N.R GROUP Co.,LTD
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    bot_api_key = fields.Char(
        string='Bank of Thailand API Client ID',
    )
    bot_rate_type = fields.Selection(
        string='Rate Type',
        selection=[('buying_sight', 'Buying Sight'),
                   ('buying_transfer', 'Buying Transfer'),
                   ('selling', 'Selling'),
                   ('mid_rate', 'Mid Rate'),
                   ], default='mid_rate'
    )
