# -*- coding: utf-8 -*-
{
    'name': "po-pending-rfq-reprot",

    'summary': """
        This Module Contain Report for Pending RFQ's
        """,
    'author': "PresevereMind",
    'website': "https://perseveremind.com",
    'category': "Custom Development",
    'version': "1.0",
    'license': "LGPL-3",

    
    'depends': ['purchase'],

    
    'data': [
        'security/ir.model.access.csv',
       
        'wizard/rfq_pending_report_wizard.xml',
        'views/views.xml',
        'report/rfq_pending_report.xml'
    ] 
}
