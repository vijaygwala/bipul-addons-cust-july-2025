# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, models, _
from odoo.exceptions import UserError


class OpenPOReportWizard(models.TransientModel):
    """Class added to pass report details."""

    _name = "open.po.report.wizard"
    _description = "Open PO Report Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    partner_ids = fields.Many2many(
        "res.partner", string="Vendor", domain="[('is_company', '=', True)]"
    )
    category_ids = fields.Many2many("product.category", string="product Category")
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id
    )
    all_vendor = fields.Boolean(string="All Vendor?", default=True)
    all_categ = fields.Boolean(string="All Category?", default=True)
    all_product = fields.Boolean(string="All Product?", default=True)
    product_ids = fields.Many2many("product.product", string="Product")
    category_partner = fields.Selection(
        [("partner", "Vendor"), ("category", "Category"), ("product", "Product")],
        string="Report for?",
        default="partner",
    )

    def print_open_po_report(self):
        """It creates pdf reports for particular vendor."""
        data_dict = {}
        if self.start_date > self.end_date:
            raise UserError(_("Start date should not be greater than end date"))
        data = self.read(
            [
                "start_date",
                "end_date",
                "all_vendor",
                "category_partner",
                "all_categ",
                "all_product",
            ]
        )[0]
        start_date = data["start_date"]
        end_date = data["end_date"]
        all_vendor = data["all_vendor"]
        category_partner = data["category_partner"]
        partner_list = self.partner_ids.ids
        category_list = self.category_ids.ids
        product_list = self.product_ids.ids
        all_categ = data["all_categ"]
        all_product = data["all_product"]
        data_dict.update(
            {
                "partner_ids": list(set(partner_list)),
                "category_ids": list(set(category_list)),
                "product_ids": list(set(product_list)),
                "start_date": start_date,
                "end_date": end_date,
                "all_vendor": all_vendor,
                "category_partner": category_partner,
                "all_categ": all_categ,
                "all_product": all_product,
               
            }
        )
        return self.env.ref("ak_open_po_report.action_report_open_po").report_action(
            self, data_dict
        )
