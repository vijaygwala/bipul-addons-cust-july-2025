from odoo import fields, models

class PosOrderLine(models.Model):

    _inherit = 'pos.order.line'
    cashier_employee_id = fields.Many2one('hr.employee', string='Cashier')
    cashier_employee_name = fields.Char(string='Cashier' ,related='cashier_employee_id.name')
    
    def _export_for_ui(self, orderline):
        result = super()._export_for_ui(orderline)

        result['cashier_employee_id'] = orderline.cashier_employee_id
        return result

    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)
        print(result)
        
        return result



class Employee(models.Model):
   

    _inherit = 'hr.employee'

    def get_employii(self):
        return self.read(['id','name'])
