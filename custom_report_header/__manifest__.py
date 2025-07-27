# -*- coding: utf-8 -*-
{
    'name': "Purchase Report Customisation & POS customer filter",

    'summary': """
Purchase Order Report Customisations and POS customer filter Customisation.
        """,

    'description': """
    This module allows to 
    1) filter the customers only in pos sessions.
    2) this module also contain the report header layout modifications.
    3) this module contain the currency symbol removed from po lines and added respective name in lines
    """,

    'author': "PresevereMind",
    'website': "https://perseveremind.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','web','point_of_sale'],

    # always loaded
    'data': [
        'views/templates.xml',
    ]
}
