{
    'name': 'Mobishastra SMS Gateway (Contacts & CRM Integration)',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Mobishastra SMS Gateway with Config Wizard and CRM/Contacts Integration',
    'author': 'ChatGPT',
    'depends': ['base', 'contacts', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'data/server_actions.xml',
        'wizard/mobishastra_config_wizard_view.xml',
        'wizard/send_sms_wizard_view.xml',
        'views/mobishastra_menu.xml',
        'views/res_partner_view.xml',
        'views/crm_lead_view.xml',
    ],
    'installable': True,
    'application': False,
}