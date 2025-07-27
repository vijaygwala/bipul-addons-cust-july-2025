# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'
    _description = 'Register Payment'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', company_dependent=True,
        help="Analytic account in which cost and revenue entries will take place for financial management of the manufacturing order.")

    def action_create_payments(self):
        payments = self._create_payments()
        active_ids = self._context.get('active_ids')
        move_ids = self.env['account.move'].browse(active_ids)
        if move_ids:
            for move in move_ids:
                if move.line_ids:
                    for line in move.line_ids:
                        line.analytic_distribution = {self.analytic_account_id.id: 100}             
        if payments:
            for payment in payments:
                payment.analytic_account_id = self.analytic_account_id
                if payment.move_id:
                    for line in payment.move_id.line_ids:
                        line.analytic_distribution = {self.analytic_account_id.id: 100}

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action

