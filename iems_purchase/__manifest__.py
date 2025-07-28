# -*- coding: utf-8 -*-
{
    'name': "IEMS Purchase",

    'summary': """
        Purchase Order Approval upto 3 levels
    """,

    'description': """
        Purchase Order Approval upto 3 levels
    """,

    'author': "IEMS Engineers",
    'website': "http://www.iemsglobal.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        'views/iems_purchase_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'assets': {

    },
    'license': 'LGPL-3',
}
