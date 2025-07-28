# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.tools.float_utils import float_round

class AccountMove(models.Model):
	_inherit = 'account.move'
	
class AccountPayment(models.Model):
	_inherit = 'account.payment'

	analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', company_dependent=True)

	def action_post(self):
		res = super(AccountPayment, self).action_post()
		if not self.env.context.get('dont_redirect_to_payments'):
			if self.move_id.line_ids:
				for line in self.move_id.line_ids:
					line.analytic_distribution = {self.analytic_account_id.id: 100}
		return res


