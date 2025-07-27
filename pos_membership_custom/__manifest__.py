# -*- coding: utf-8 -*-
{
    'name': "pos_membership_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
         'views/res_partner_view.xml',
        'views/pos_order.xml',
        'views/customer_membership_views.xml',
        'views/res_config_settings_views.xml',
        'data/cron.xml'
        
    ],
    'assets': {
        'point_of_sale.assets': [
           "pos_membership_custom/static/src/xml/ProductScreenButtons.xml",
           "pos_membership_custom/static/src/xml/popup.xml",
           "pos_membership_custom/static/src/xml/PartnerDetailsEdit.xml",
           "pos_membership_custom/static/src/js/customer_validation.js",
           "pos_membership_custom/static/src/js/CreateMembership.js",
            "pos_membership_custom/static/src/js/mebership_ref_order.js",
           "pos_membership_custom/static/src/js/Popup-verify.js",
            "pos_membership_custom/static/src/js/VerifyMembership.js",
            "pos_membership_custom/static/src/js/PosConfig.js",
             "pos_membership_custom/static/src/js/AbstractAwaitablePopup.js",
             "pos_membership_custom/static/src/css/custom-style.scss"
        ],
         'web.assets_backend': [
       "pos_membership_custom/static/src/css/backedn_dropdown.scss",
    ],
    }
  
}
