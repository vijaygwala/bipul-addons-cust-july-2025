from odoo import models ,fields, api
class MobishastraSMS(models.AbstractModel):
    _name = 'mobishastra.sms'
    _description = 'Mobishastra SMS Logic'



class MobishastraSMSLog(models.Model):
    _name = 'mobishastra.sms.log'
    _description = 'Mobishastra SMS Log'
    _order = 'create_date desc'

    mobile = fields.Char('Mobile Number', required=True)
    message = fields.Text('Message', required=True)
    route = fields.Selection([
        ('Promotional', 'Promotional'),
        ('Transactional', 'Transactional')
    ], string='Route', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Status', default='pending', required=True)
    status_code = fields.Char('HTTP Status Code')
    response_text = fields.Text('API Response')
    create_date = fields.Datetime('Created On', readonly=True)
    created_by = fields.Many2one('res.users', string='Sent By', default=lambda self: self.env.user)

    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.mobile or ''} - {rec.status.upper()}"
            res.append((rec.id, name))
        return res
