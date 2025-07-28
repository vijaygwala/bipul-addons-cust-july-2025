from odoo import models, fields, api

class PendingRFQWizard(models.TransientModel):
    _name = 'pending.rfq.report.wizard'
    _description = 'Pending RFQs'


    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('l2', 'L2 Apporoved'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
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

        

        return self.env.ref('pending_rfq_report.pending_rfq_report_action').report_action(self, data=data)



class PendingRFQPDF(models.AbstractModel):
    _name = 'report.pending_rfq_report.pending_rfq_report'

    def _get_report_values(self, docids, data=None):
        """
        @Description : Report Data Preprocessing
        @author : Vijay Gwala
        @param : self,docids,data
        @return type : Report Context Data
        """
        domain = [('state','=',data['state'])]
        if data['from_date'] and data['to_date']:
            domain.append(('date_order', '>=', data['from_date']))
            domain.append(('date_order','<=',data['to_date']))
        orders = self.env['purchase.order'].sudo().search(domain)
        
       
        
        return {
            'doc_ids': orders.ids,
            'doc_model': 'purchase.order',
            'docs': orders,
            'datas': data,
            'db_data':orders.retrieve_dashboard()
        }