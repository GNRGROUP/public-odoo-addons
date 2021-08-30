# Copyright 2021 G.N.R GROUP Co.,LTD
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

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
