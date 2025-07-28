from odoo import models, fields, api,_

class PaymentCycleWizard(models.TransientModel):
    _name = 'payment.cycle.report.wizard'
    _description = 'Payment Cycle'


    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    


    def action_print(self):
        """
        @Description : Generate PDF report
        @author : Vijay Gwala 
        @param : self
        @return type : action[ir.action.report]
        """
        data={
                'from_date': self.from_date,
                'to_date': self.to_date,
               'state':self.state
              }

        

        return self.env.ref('payment_cycle_report.payment_cycle_report_action').report_action(self, data=data)



class PaymentCyclePDF(models.AbstractModel):
    _name = 'report.payment_cycle_report.payment_cycle_report'

    def _get_report_values(self, docids, data=None):
        """
        @Description : Report Data Preprocessing
        @author : Vijay Gwala
        @param : self,docids,data
        @return type : Report Context Data
        """
        domain = [('payment_type','=','outbound')]
        if data['state']:
            domain.append(('state', '=', data['state']))
            
        if data['from_date'] and data['to_date']:
            domain.append(('date', '>=', data['from_date']))
            domain.append(('date','<=',data['to_date']))

        payments = self.env['account.payment'].sudo().search(domain)
        
        data['PC'] = self.env['ir.sequence'].next_by_code('payment.cycle.report.wizard') or _('New')
        
        return {
            'doc_ids': payments.ids,
            'doc_model': 'account.payment',
            'docs': payments,
            'datas': data
        }