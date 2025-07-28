# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
# Aktiv Software:
#   - Heli Kantawala
#   - Baldev Bharvadiya
#   - Helly Kapatel

{
    "name": "Open PO or Product not received report",
    "category": "Purchases",
    "summary": "Get Open Purchase Order or Product not received Report.",
    "version": "16.0.1.0.0",
    "website": "https://aktivsoftware.com",
    "author": "Aktiv Software",
    "description": """This module will allow users to print and display those purchase order details
        report which are confirmed but not yet received.""",
    "license": "OPL-1",
    "depends": ["purchase_stock"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/open_po_report_wizard.xml",
        "reports/report.xml",
        "reports/report_open_po.xml",
    ],
    "images": [
        "static/description/banner.jpg",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "currency": "USD",
    "price": 10,
    }
