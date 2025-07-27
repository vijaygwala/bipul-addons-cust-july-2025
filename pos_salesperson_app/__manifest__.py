# -*- coding: utf-8 -*-
{
    "name" : "Assign Sales Person on POS - Point of Sales Sales Person",
    "author": "Edge Technologies",
    "version" : "16.0.1.0",
    "live_test_url":'https://youtu.be/wFi7LozPsTc',
    "images":["static/description/main_screenshot.png"],
    'summary': 'POS salesperson for pos order sales person point of sales sales person pos sales person for pos saleperson for point of sales assign sales person for pos assign sales person for point of sale sale person pos salesman assign salesman on point of sale orders.',
    "description": """
        This app used to add sales person from the pos screen.

    """,
    "license" : "OPL-1",
    "depends" : ['base','point_of_sale'],
    "data": [
        'views/pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_salesperson_app/static/src/css/custom.css',
            'pos_salesperson_app/static/src/js/Orderline.js',
            'pos_salesperson_app/static/src/js/SalesPersonPopupWidget.js',
            'pos_salesperson_app/static/src/js/pos.js',
            'pos_salesperson_app/static/src/xml/pos.xml',
        ],              
    },
    "auto_install": False,
    "price": 20,
    "currency": 'EUR',
    "installable": True,
    "category" : "Point of Sale",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
