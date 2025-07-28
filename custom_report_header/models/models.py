# -*- coding: utf-8 -*-

from odoo import models, fields, api
from markupsafe import Markup


    
class PosSessionInherited(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_res_partner(self, params):
        if not self.config_id.limited_partners_loading:
            return self.env['res.partner'].search_read(**params['search_params'])
        partner_ids = [res[0] for res in self.config_id.get_limited_partners_loading()]
        params['search_params']['domain'] = [('id', 'in', partner_ids),('customer_rank','>',0)]
        return self.env['res.partner'].search_read(**params['search_params'])