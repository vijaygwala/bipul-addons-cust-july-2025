# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


    
class PurchaseOrderInherited(models.Model):
    _inherit = 'purchase.order'

    @property
    def get_total_company_currency(self):
        
        return self.currency_id._convert(self.amount_total,self.company_id.currency_id,self.env.company,datetime.today())
      