import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SendSMSWizard(models.TransientModel):
    _name = 'send.sms.wizard'
    _description = 'Send SMS Wizard'

    mobile = fields.Char('Mobile Number', required=True)
    message = fields.Text('Message', required=True)
    use_promotional = fields.Boolean('Use Promotional Route')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')
        if active_model and active_id:
            record = self.env[active_model].browse(active_id)
            if hasattr(record, 'mobile'):
                res['mobile'] = record.mobile
            elif hasattr(record, 'phone'):
                res['mobile'] = record.phone
        return res

    def action_send_sms(self):
        params = self.env['ir.config_parameter'].sudo()
        api_url = params.get_param('mobishastra.api_url')
        sender_id = params.get_param('mobishastra.sender_id')
        transactional_user = params.get_param('mobishastra.transactional_user')
        transactional_pwd = params.get_param('mobishastra.transactional_pwd')
        promotional_user = params.get_param('mobishastra.promotional_user')
        promotional_pwd = params.get_param('mobishastra.promotional_pwd')

        user = promotional_user if self.use_promotional else transactional_user
        pwd = promotional_pwd if self.use_promotional else transactional_pwd

        if not api_url or not user or not pwd or not sender_id:
            raise UserError(_('Please configure Mobishastra credentials first in Technical -> Mobishastra Config.'))

        payload = {
            'user': user,
            'pwd': pwd,
            'senderid': sender_id,
            'mobileno': self.mobile,
            'msgText': self.message,
            'CountryCode': 'All'
        }

        try:
            response = requests.get(api_url, params=payload, timeout=10)
            if response.status_code != 200:
                raise UserError(_('Failed to send SMS: %s') % response.text)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('SMS Sent'),
                    'message': _('Response: %s') % response.text,
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            raise UserError(_('Error while sending SMS: %s') % str(e))