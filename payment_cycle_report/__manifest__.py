# -*- coding: utf-8 -*-
{
    'name': "Payment Cycle Report",

    'summary': """
        This Module Contain Report for Payment Cycle's
        """,
    'author': "PresevereMind",
    'website': "https://perseveremind.com",
    'category': "Custom Development",
    'version': "1.0",
    'license': "LGPL-3",

    
    'depends': ['account_accountant','ak_open_po_report'],

    
    'data': [
        'security/ir.model.access.csv',
       
        'wizard/payment_cycle_report_wizard.xml',
        'views/views.xml',
        'report/payment_cycle_report.xml'
    ] 
}
