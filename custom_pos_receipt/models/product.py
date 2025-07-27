
from odoo import models, fields, api, _

class product_template(models.Model):
	_inherit = 'product.template'

	name_arabic = fields.Char(string="Arabic Name")


class PosOrder(models.Model):
	_inherit = 'pos.order'

	order_barcode = fields.Char(string="Order Barcode")

	@api.model
	def _order_fields(self, ui_order):
		res = super(PosOrder, self)._order_fields(ui_order)
		res['order_barcode'] = ui_order.get('order_barcode',False)
		return res


class PosSession(models.Model):
	_inherit = 'pos.session'



	def _loader_params_product_product(self):
		result = super()._loader_params_product_product()
		result['search_params']['fields'].extend(['name','name_arabic'])
		return result


	def _loader_params_res_company(self):
		result = super()._loader_params_res_company()
		result['search_params']['fields'].extend(['street','street2','city','state_id','vat'])
		return result