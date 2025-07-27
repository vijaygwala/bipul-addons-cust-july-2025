# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'POS Custom Receipt',
    'category': 'Sales/Point of Sale',
    'summary': 'This module is used to customized receipt of point of sale when a user adds a product in the cart and validates payment and print receipt, then the user can see the client name on POS Receipt. | Custom Receipt | POS Reciept | Payment | POS Custom Receipt',
    'description': "Customized our point of sale receipt",
    'version': '16.0.1.0',
    'website': 'https://www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'images': ['static/description/banner.jpg'],
    'depends': ['base', 'point_of_sale', 'l10n_gcc_pos', 'l10n_sa_pos', 'l10n_co_pos'], 
    'data': ['views/product_view.xml'],

    'assets': {
        'point_of_sale.assets': [
            "custom_pos_receipt/static/src/js/models.js",
            "custom_pos_receipt/static/src/xml/pos.xml",
	    "custom_pos_receipt/static/src/css/arabic_font.css",
            "custom_pos_receipt/static/src/js/JsBarcode.all.min.js",
            "custom_pos_receipt/static/src/js/OrderReceipt.js",            
        ],
    },
    'installable': True,
}
