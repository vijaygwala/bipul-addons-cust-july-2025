import requests
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MobishastraConfigWizard(models.TransientModel):
    _name = 'mobishastra.config.wizard'
    _description = 'Mobishastra Configuration Wizard'

    api_url = fields.Char('API URL', default='https://saudi.mshastra.com/sendurl.aspx', required=True)
    sender_id = fields.Char('Sender ID', required=True)
    transactional_user = fields.Char('Transactional User ID', required=True)
    transactional_pwd = fields.Char('Transactional Password', required=True)
    promotional_user = fields.Char('Promotional User ID')
    promotional_pwd = fields.Char('Promotional Password')

    # Test send section
    test_mobile = fields.Char('Test Mobile Number')
    test_message = fields.Text('Test Message', default='Hello How are you')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        params = self.env['ir.config_parameter'].sudo()
        res.update({
            'api_url': params.get_param('mobishastra.api_url', 'https://saudi.mshastra.com/sendurl.aspx'),
            'sender_id': params.get_param('mobishastra.sender_id', 'MSGworld'),
            'transactional_user': params.get_param('mobishastra.transactional_user', 'MansamTRK'),
            'transactional_pwd': params.get_param('mobishastra.transactional_pwd', '9pph_y49'),
            'promotional_user': params.get_param('mobishastra.promotional_user', 'MansamPRK'),
            'promotional_pwd': params.get_param('mobishastra.promotional_pwd', 'ujejumme'),
        })
        return res

    def action_save_config(self):
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('mobishastra.api_url', self.api_url)
        params.set_param('mobishastra.sender_id', self.sender_id)
        params.set_param('mobishastra.transactional_user', self.transactional_user)
        params.set_param('mobishastra.transactional_pwd', self.transactional_pwd)
        params.set_param('mobishastra.promotional_user', self.promotional_user)
        params.set_param('mobishastra.promotional_pwd', self.promotional_pwd)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Mobishastra configuration saved successfully.'),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_test_send(self):
        if not self.test_mobile or not self.test_message:
            raise UserError(_('Please provide both test mobile and message.'))

        payload = {
            'user': self.transactional_user,
            'pwd': self.transactional_pwd,
            'senderid': self.sender_id,
            'mobileno': self.test_mobile,
            'msgText': self.test_message,
            'CountryCode': 'All'
        }
        try:
            response = requests.get(self.api_url, params=payload, timeout=10)
            if response.status_code != 200:
                raise UserError(_('SMS sending failed: %s') % response.text)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Test SMS Sent'),
                    'message': _('Response: %s') % response.text,
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            raise UserError(_('Error while sending test SMS: %s') % str(e))