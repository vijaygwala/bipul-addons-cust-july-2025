# -*- coding: utf-8 -*-
from odoo import models, fields


class PosSession(models.Model):
    _inherit = 'pos.session'

    account_analytic_id = fields.Many2one('account.analytic.account',
        related="config_id.account_analytic_id",
        store=True, string='Analytic Account', copy=False
    )

    def _get_stock_expense_vals(self, exp_account, amount, amount_converted):
        res = super(PosSession, self)._get_stock_expense_vals(exp_account, amount, amount_converted)
        res['analytic_distribution'] = { self.account_analytic_id.id: 100}
        return res

    def _get_stock_output_vals(self, out_account, amount, amount_converted):
        res = super(PosSession, self)._get_stock_output_vals(out_account, amount, amount_converted)
        res['analytic_distribution'] = { self.account_analytic_id.id: 100}
        return res

    def _prepare_line(self, order_line):
        res = super(PosSession, self)._prepare_line(order_line)
        res['analytic_distribution'] = { order_line.order_id.account_analytic_id.id: 100}
        return res

    def _get_sale_vals(self, key, amount, amount_converted):
        res = super(PosSession, self)._get_sale_vals(key, amount, amount_converted)
        res['analytic_distribution'] = { self.account_analytic_id.id: 100}
        return res

    def _get_invoice_receivable_vals(self, amount, amount_converted):
        res = super(PosSession, self)._get_invoice_receivable_vals(amount, amount_converted)
        res['analytic_distribution'] = { self.account_analytic_id.id: 100}
        return res

    def _validate_session(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        res = super(PosSession, self)._validate_session(balancing_account=balancing_account, amount_to_balance=amount_to_balance, bank_payment_method_diffs=bank_payment_method_diffs)
        all_moves = self._get_related_account_moves()
        all_moves.mapped('line_ids').write({'analytic_distribution': { self.account_analytic_id.id: 100}})
        return res
