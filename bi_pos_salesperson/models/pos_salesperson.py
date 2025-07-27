# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, tools


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_cashier = fields.Boolean('Allow Cashier')
    allow_user_ids = fields.Many2many('res.users')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_cashier = fields.Boolean(related='pos_config_id.allow_cashier',readonly=False)
    allow_user_ids = fields.Many2many(related='pos_config_id.allow_user_ids',readonly=False)

    
class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    customer_id = fields.Many2one('res.users', string='Cashier')
    customer_name = fields.Char('Customer Name' ,related='customer_id.name')


    def _export_for_ui(self, orderline):
        return {
            'qty': orderline.qty,
            'price_unit': orderline.price_unit,
            'price_subtotal': orderline.price_subtotal,
            'price_subtotal_incl': orderline.price_subtotal_incl,
            'product_id': orderline.product_id.id,
            'discount': orderline.discount,
            'tax_ids': [[6, False, orderline.tax_ids.mapped(lambda tax: tax.id)]],
            'id': orderline.id,
            'pack_lot_ids': [[0, 0, lot] for lot in orderline.pack_lot_ids.export_for_ui()],
            'customer_note': orderline.customer_note,
            'refunded_qty': orderline.refunded_qty,
            'price_extra': orderline.price_extra,
            'refunded_orderline_id': orderline.refunded_orderline_id,
            'full_product_name': orderline.full_product_name,
            'customer_id': orderline.customer_id.id,
            'customer_name': orderline.customer_name
        }


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    customer_id = fields.Many2one('res.users', string='PoS Cashier', store=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + ", l.customer_id as customer_id"

    def _from(self):
        return super(PosOrderReport, self)._from() + " LEFT JOIN pos_order_line v ON (v.id=l.customer_id)"

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ", l.customer_id"


class POSOrderLoad(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_users(self):
        result = super()._loader_params_res_users()
        result['search_params']['fields'].extend(['name','id'])
        return result


    def load_pos_data(self):
        loaded_data = {}
        self = self.with_context(loaded_data=loaded_data)
        for model in self._pos_ui_models_to_load():
            loaded_data[model] = self._load_model(model)
        self._pos_data_process(loaded_data)        
        users_data = self._get_pos_ui_pos_res_users(self._loader_params_pos_res_users())
        loaded_data['users'] = users_data
        return loaded_data


    def _get_pos_ui_pos_res_users(self, params):
        users = self.env['res.users'].search_read(**params['search_params'])
        return users


    def _loader_params_pos_res_users(self):
        return {
            'search_params': {
                'domain': [],
                'fields': ['name','id'],
            },
        }