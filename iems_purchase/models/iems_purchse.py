# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo import models, fields, api, _
import base64
from io import BytesIO
import xlwt
from markupsafe import Markup
import html2text
from PIL import Image
import os

directory = os.path.dirname(__file__)


class IemsPurchase(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'L1 Approved'),
        ('l2', 'L2 Approved'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_approve(self, force=False):
        if self._approval_allowed():
            print('approval k ander aaya')
            self.write({'state': 'purchase', 'date_approve': fields.Datetime.now()})
            self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        else:
            print('approval k ander nhi aya')
        return {}

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                print("returning true")
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def button_confirm_l2(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'to approve']:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'l2'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def _approval_allowed(self):
        """Returns whether the order qualifies to be approved by the current user"""
        self.ensure_one()
        
        return ( (
                self.amount_total >= self.env.company.currency_id._convert(
                    self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
                    self.date_order or fields.Date.today())
                ) and ( self.user_has_groups('iems_purchase.group_purchase_l3') and self.state =='l2'))


class IemsCompany(models.Model):
    _inherit = 'res.company'

    po_double_validation = fields.Selection([
        ('one_step', 'Confirm purchase orders in one step'),
        ('two_step', 'Get 2 levels of approvals to confirm a purchase order'),
        ('three_step', 'Get 3 levels of approvals to confirm a purchase order')
    ], string="Levels of Approvals", default='one_step',
        help="Provide a triple validation mechanism for purchases")


class IemsResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    po_order_approval = fields.Boolean("Purchase Order Approval",
                                       default=lambda self: self.env.company.po_double_validation == 'three_step')

    def set_values(self):
        super().set_values()
        po_lock = 'lock' if self.lock_confirmed_po else 'edit'
        po_double_validation = 'three_step' if self.po_order_approval else 'one_step'
        if self.po_lock != po_lock:
            self.po_lock = po_lock
        if self.po_double_validation != po_double_validation:
            self.po_double_validation = po_double_validation


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


class PurchaseBillUnion(models.Model):
    _inherit = 'purchase.bill.union'


class PurchaseReport(models.Model):
    _inherit = 'purchase.report'
