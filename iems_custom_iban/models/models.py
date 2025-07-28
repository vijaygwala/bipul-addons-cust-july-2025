# -*- coding: utf-8 -*-

from odoo import models, fields, api



    
class ResPartnerBankInherited(models.Model):
    _inherit = 'res.partner.bank'

    iban_custom = fields.Char(string='IBAN')

    