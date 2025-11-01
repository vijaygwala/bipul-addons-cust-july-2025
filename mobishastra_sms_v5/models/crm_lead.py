from odoo import models, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_open_sms_wizard(self):
        self.ensure_one()
        return {
            'name': _('Send SMS'),
            'type': 'ir.actions.act_window',
            'res_model': 'send.sms.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mobile': self.phone or self.mobile,
            }
        }
