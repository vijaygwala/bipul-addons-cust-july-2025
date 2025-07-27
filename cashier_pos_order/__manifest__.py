
{
    'name': 'Cashier In Pos Orders',
    'Version': '16.0.1.0.0',
    'category': 'Extra Tools',
  
    'description': 'This module allows you to assign cashier to orders in the Point of Sale (POS)',
    'author': 'vijay gwala',
    'company': 'vijay gwala',
    'depends': ['point_of_sale','bi_pos_salesperson'],
    'data': [
        'views/pos_order.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'cashier_pos_order/static/src/js/pos_load_data.js',
            'cashier_pos_order/static/src/js/order_line_user.js',
            'cashier_pos_order/static/src/js/pos_screen.js',
            'cashier_pos_order/static/src/js/pos_order.js',
            'cashier_pos_order/static/src/js/pos_popup.js',
            'cashier_pos_order/static/src/xml/pos_screen_templates.xml',
            'cashier_pos_order/static/src/xml/pos_popup_templates.xml',
            
        ],

    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
