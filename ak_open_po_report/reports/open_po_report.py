from datetime import datetime

from odoo import api, models
from datetime import datetime,date,timedelta


class OpenPoReport(models.AbstractModel):
    """Class call to add open po report."""

    _name = "report.ak_open_po_report.report_open_po"
    _description = "Open PO report"

    def get_filtered_data(self, partner, data, partner_dict, line):
        """Purchase order details dict"""
        
        
        purchase_line_vals = {
            "create_date": line.order_id.create_date.date(),
            "purchase_order": line.order_id.name,
            "product": line.product_id.name,
            "categ_id": line.product_id.categ_id.complete_name,
            "product_qty": line.product_qty,
            "qty_received": line.qty_received,
            "partner_name": line.partner_id.name,
            "partner_ref": line.order_id.partner_ref,
            "prod_qty_subtotal": (line.product_qty * line.price_unit) + (line.taxes_id.amount/100)*(line.product_qty * line.price_unit) if line.taxes_id else (line.product_qty * line.price_unit) ,
            "received_subtotal": (line.qty_received * line.price_unit) + (line.taxes_id.amount/100)*(line.qty_received * line.price_unit) if line.taxes_id else (line.qty_received * line.price_unit),
            "receipt_status": "Ready",
            "aging": line.order_id.payment_term_id.name,
            "pending_qty": line.product_qty - line.qty_received,
            "pending_qty_value":((line.product_qty-line.qty_received) * line.price_unit) + (line.taxes_id.amount/100)*((line.product_qty-line.qty_received) * line.price_unit) if line.taxes_id else ((line.product_qty-line.qty_received) * line.price_unit),
            "curr":line.order_id.currency_id
        }
        # Prepared order line
        if partner not in partner_dict.keys():
            partner_dict.update(
                {
                    partner: {
                        "order_line": [purchase_line_vals],
                    }
                }
            )
        else:
            partner_dict[partner]["order_line"].append(purchase_line_vals)
        # Passed all values to report
        new_dict = {
            "categ_partner": data["category_partner"],
            "start_date": data["start_date"],
            "end_date": data["end_date"],
        }
        return new_dict

    def get_purchase_order_data(self, filtered_data):
        """Prepare Order Line which satisfies the Conditions"""
        for move in [
            moves for moves in filtered_data["line"].order_id.picking_ids.move_line_ids
        ]:
            if (
                move.product_id == filtered_data["line"].product_id
                and move.state == "assigned"
            ):
                new_dict = self.get_filtered_data(
                    filtered_data["partner"],
                    filtered_data["data"],
                    filtered_data["partner_dict"],
                    filtered_data["line"],
                )
                filtered_data["partner_dict"][filtered_data["partner"]].update(new_dict)

    def get_po_line_details(self, data):
        """Get Purchase order line details."""
        partner_dict = {}
        start_date = data["start_date"]
        end_date = data["end_date"]
        partner_obj = self.env["res.partner"]
        order_line = self.env["purchase.order.line"]
        # Filtered domain
        domain = [
            ("order_id.date_order", ">=", start_date),
            ("order_id.date_order", "<=", end_date),
            ("order_id.state", "in", ["purchase"]),
        ]
        # Report data for partner
        if data["category_partner"] == "partner":
            if data["all_vendor"]:
                all_partner_ids = partner_obj.search([])
                for partner in all_partner_ids:
                    domain.extend([("order_id.partner_id", "=", partner.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
            else:
                partner_ids = self.env["res.partner"].browse(data["partner_ids"])
                for partner in partner_ids:
                    domain.extend([("order_id.partner_id", "=", partner.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
        # Report data for category
        if data["category_partner"] == "category":
            if data["all_categ"]:
                all_categ_ids = self.env["product.category"].search([])
                for category in all_categ_ids:
                    partner = category
                    domain.extend([("product_id.categ_id", "=", category.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
            else:
                categ_ids = self.env["product.category"].browse(data["category_ids"])
                for category in categ_ids:
                    partner = category
                    domain.extend([("product_id.categ_id", "=", category.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
        # Report data for product
        if data["category_partner"] == "product":
            # When all product
            if data["all_product"]:
                all_product_ids = self.env["product.product"].search([])
                for product in all_product_ids:
                    partner = product
                    domain.extend([("product_id.id", "=", product.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
            else:
                # when selective report
                product_ids = self.env["product.product"].browse(data["product_ids"])
                for product in product_ids:
                    partner = product
                    domain.extend([("product_id.id", "=", product.id)])
                    purchase_line_data = order_line.search(domain)
                    for line in purchase_line_data.filtered(
                        lambda l: l.qty_received < l.product_qty
                    ).sorted(key=lambda p: (p.product_id.name)):
                        if line.order_id.picking_ids:
                            filtered_data = {
                                "partner": partner,
                                "data": data,
                                "partner_dict": partner_dict,
                                "line": line,
                            }
                            self.get_purchase_order_data(filtered_data)
                    domain.pop()
        return partner_dict

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get wizard value i.e date, group by option etc."""
        lang_code = self.env.context.get("lang") or "en_US"
        lang = self.env["res.lang"]
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        categ_ids = partner_ids = product_ids = None
        data.update(self._context)
        if data.get("category_partner") == "partner":
            partner_ids = data.get("partner_ids")
        elif data.get("category_partner") == "category":
            categ_ids = data.get("category_ids")
        elif data.get("category_partner") == "product":
            product_ids = data.get("product_ids")
        lines_data = self.get_po_line_details(data)
        # for partner,obj in lines_data.items():
        #     for rec in obj['order_line']:
        #         po = self.env['purchase.order'].sudo().search([('name','=',rec['purchase_order'])])
        #         rec.update({'partner_name': partner.name})
        #         rec.update({'partner_ref': po.partner_ref})
        #         po.order_line.filtered()
        # return value to xml side.
        return {
            "doc_ids": docids,
            "doc_model": "purchase.order",
            "docs_partner": self.env["res.partner"].browse(partner_ids),
            "docs_categ": self.env["product.category"].browse(categ_ids),
            "date": datetime.now().strftime(date_format),
            "lines_data": lines_data,
        }
