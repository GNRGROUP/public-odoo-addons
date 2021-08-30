
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bot_api_key = fields.Char(
        string='API Key',
        related='company_id.bot_api_key',
        readonly=False,
    )
    bot_rate_type = fields.Selection(
        string='Rate Type',
        related='company_id.bot_rate_type',
        readonly=False,
    )
