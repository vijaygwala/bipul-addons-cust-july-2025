# -*- coding: utf-8 -*-
{
    'name': "IBAN Custom Field",

    'summary': """
This module will add an IBAN field in the partners>>Accounting>>Bank Accounts
        """,

    'description': """
    This module allows to 
    1) Add an IBAN field in the Vendor master in Accounting Tab under the Bank Details Tree View 
    """,

    'author': "PresevereMind",
    'website': "https://perseveremind.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','account'],

    # always loaded
    'data': [
        'views/templates.xml',
    ]
}
