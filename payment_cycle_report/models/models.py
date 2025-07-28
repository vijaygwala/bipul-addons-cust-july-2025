# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


    
class AccountPaymentInherited(models.Model):
    _inherit = 'account.payment'

    @property
    def get_amount_in_lc(self):
        
        return self.currency_id._convert(self.amount,self.company_id.currency_id,self.env.company,self.date)
      
    @property
    def get_purchase_orders(self):
        res = self.button_open_bills()
        if res.get('res_id',False):
            bills = self.env['account.move'].sudo().browse(res['res_id'])
        else:
            bills = self.env['account.move'].sudo().search(res.get('domain')) if res.get('domain') else []

        po_data = {'po_name':[],'po_dates':[],'po_ref':[]}
        for bill in bills:
            res = bill.action_view_source_purchase_orders()
            orders = []
            if res.get('res_id',False):
                orders = self.env['purchase.order'].sudo().browse(res['res_id'])
            else:
                orders = self.env['purchase.order'].sudo().search(res.get('domain')) if res.get('domain') else []
            po_data['po_name'] += [o.name for o in orders if o.name]
            po_data['po_dates'] += [o.date_order.strftime('%d %B, %Y') for o in orders if o.date_order]
            po_data['po_ref'] += [o.partner_ref for o in orders if o.partner_ref]
            
        po_data['po_name'] =','.join(po_data['po_name']) if po_data['po_name'] else ''
        po_data['po_dates'] = ','.join(po_data['po_dates']) if po_data['po_dates'] else ''
        po_data['po_ref'] = ','.join(po_data['po_ref']) if po_data['po_ref'] else ''
        
        return po_data
    