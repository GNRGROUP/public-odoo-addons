# -*- coding: utf-8 -*-
{
    'name': "currency_rate_update_bot",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "krisa",
    'website': "https://github.com/GNRGROUP/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Financial Management/Configuration',
    'version': '14.0.1.0.2',

    # any module necessary for this one to work correctly
    'depends': ['currency_rate_update'],

    # always loaded
    'data': [
        'views/res_config_settings.xml',
    ],
    'installable': True,
    'application': False,
}
