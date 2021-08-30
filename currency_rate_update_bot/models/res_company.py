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
