import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SendSMSWizard(models.TransientModel):
    _name = 'send.sms.wizard'
    _description = 'Send SMS Wizard'

    mobile = fields.Char('Mobile Number(s) separated by Comma', required=True)
    message = fields.Text('Message', required=True)
    use_promotional = fields.Boolean('Use Promotional Route')

    # ------------------------------------------------------------
    # Defaults
    # ------------------------------------------------------------
    @api.model
    def default_get(self, fields_list):
        """Prefill comma-separated mobile numbers for selected records."""
        res = super().default_get(fields_list)
        active_model = self._context.get('active_model')
        active_ids = self._context.get('active_ids', [])

        if active_model and active_ids:
            records = self.env[active_model].browse(active_ids)
            mobiles = []

            for record in records:
                number = False
                if hasattr(record, 'mobile') and record.mobile:
                    number = record.mobile
                elif hasattr(record, 'phone') and record.phone:
                    number = record.phone

                if number:
                    cleaned = number.strip().replace(' ', '').replace('+', '')
                    if cleaned not in mobiles:
                        mobiles.append(cleaned)

            if mobiles:
                res['mobile'] = ','.join(mobiles)

        return res


    # ------------------------------------------------------------
    # Internal Helpers (Reusable)
    # ------------------------------------------------------------
    def _get_mobishastra_credentials(self):
        """Fetch and validate Mobishastra configuration."""
        params = self.env['ir.config_parameter'].sudo()
        creds = {
            'api_url': params.get_param('mobishastra.api_url'),
            'sender_id': params.get_param('mobishastra.sender_id'),
            'sender_id_pramotional': params.get_param('mobishastra.sender_id_pramotional'),
            'transactional_user': params.get_param('mobishastra.transactional_user'),
            'transactional_pwd': params.get_param('mobishastra.transactional_pwd'),
            'promotional_user': params.get_param('mobishastra.promotional_user'),
            'promotional_pwd': params.get_param('mobishastra.promotional_pwd'),
        }

        if not all([creds['api_url'], creds['sender_id'], creds['transactional_user'], creds['transactional_pwd']]):
            raise UserError(_('Please configure Mobishastra credentials first in Technical → Mobishastra Config.'))
        return creds

    def _prepare_payload(self, mobile, message, creds, use_promotional):
        """Prepare API payload for Mobishastra request."""
        user = creds['promotional_user'] if use_promotional else creds['transactional_user']
        pwd = creds['promotional_pwd'] if use_promotional else creds['transactional_pwd']
        return {
            'user': user,
            'pwd': pwd,
            'senderid': creds['sender_id'] if not use_promotional else creds['sender_id_pramotional'],
            'mobileno': mobile,
            'msgText': message,
            'CountryCode': 'All',
        }

    def _create_sms_log(self, mobile, message, route):
        """Create a new SMS log record."""
        return self.env['mobishastra.sms.log'].sudo().create({
            'mobile': mobile,
            'message': message,
            'route': route,
            'status': 'pending',
        })

    def _send_request(self, api_url, payload):
        """Send GET request to Mobishastra API."""
        try:
            return requests.get(api_url, params=payload, timeout=10)
        except Exception as e:
            _logger.exception("Mobishastra API request failed: %s", e)
            raise UserError(_('Connection error while sending SMS: %s') % str(e))

    # ------------------------------------------------------------
    # Reusable Method (Can be called anywhere)
    # ------------------------------------------------------------
    @api.model
    def send_sms(self, mobile, message, use_promotional=False):
        """
        Core reusable SMS sender.
        Can be called from other models or wizards like:
            self.env['send.sms.wizard'].send_sms('9876543210', 'Hello!', False)
        """
        creds = self._get_mobishastra_credentials()
        route = 'Promotional' if use_promotional else 'Transactional'

        # Clean and split multiple numbers
        mobiles = [m.strip().replace(' ', '').replace('+', '') for m in mobile.split(',') if m.strip()]
        if not mobiles:
            raise UserError(_('Please enter at least one valid mobile number.'))

        for mob in mobiles:
            payload = self._prepare_payload(mob, message, creds, use_promotional)
            sms_log = self._create_sms_log(mob, message, route)
            response = self._send_request(creds['api_url'], payload)

            sms_log.write({
                'response_text': response.text,
                'status_code': response.status_code,
            })

            if response.status_code != 200 or any(x in response.text for x in ['Error', 'Invalid']):
                sms_log.status = 'failed'
                _logger.warning("Failed to send SMS to %s: %s", mob, response.text)
                continue  # move to next number instead of stopping the loop

            sms_log.status = 'success'
            _logger.info("SMS sent successfully to %s. Response: %s", mob, response.text[:100])

    # ------------------------------------------------------------
    # Wizard Button Action
    # ------------------------------------------------------------
    def action_send_sms(self):
        """Called when user clicks 'Send SMS' in the wizard UI."""
        for wizard in self:
            wizard.send_sms(
                mobile=wizard.mobile,
                message=wizard.message,
                use_promotional=wizard.use_promotional,
            )

            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('SMS Sent'),
                'message': _('SMS sent successfully. Check SMS Logs for details.'),
                'type': 'success',
                'sticky': False,
            }
        }
