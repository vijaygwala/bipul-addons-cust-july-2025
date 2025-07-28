# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Salesperson on POS Orders',
    "version" : "16.0.0.4",
    'category': 'Point of Sale',
    'summary': 'POS Sales person POS Salesperson assign sales person on pos order assign salesperson on pos order sales person on pos screen sales person pos sale person pos representative pos cashier on pos user point of sale cashier on point of sales person pos cashiers',
    'description': """
         This odoo app helps user to add cashier on pos order for specific product, User can add, update or remove cashier from pos screen, User can also see added cashier on pos order and see pos cashier on pos order pivot analysis report.

	pos salesperson
	pos cashier
	add cashier on pos order
	update cashier on pos order
	cashier on point of sale
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 15,
    "currency": 'EUR',
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/pos_salesperson_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            "bi_pos_salesperson/static/src/js/order_line_user.js",
            "bi_pos_salesperson/static/src/js/salesperson.js",
            "bi_pos_salesperson/static/src/js/pos_salesperson_button.js",
            "bi_pos_salesperson/static/src/js/OrderlineDetails.js",
            "bi_pos_salesperson/static/src/js/TicketScreen.js",
            'bi_pos_salesperson/static/src/xml/pos_salesperson_button.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/nM5YWHWI6Nc',
    "images": ['static/description/Banner.gif'],
    'license': 'OPL-1',
}
