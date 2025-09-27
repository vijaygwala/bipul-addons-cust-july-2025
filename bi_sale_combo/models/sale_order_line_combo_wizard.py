from odoo import models, fields, api, _

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     is_pack = fields.Boolean(string='Is Combo Product')
#     pack_ids = fields.One2many(comodel_name='product.pack', inverse_name='bi_product_template', string='Product pack')
#     combo_limit = fields.Integer(string='Combo Limitation')
#     optional_limit_qty = fields.Integer(string='Optional Combo Limitation', default=1)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    show_configure_button = fields.Boolean(
        compute="_compute_show_configure_button",
        store=False
    )

    @api.depends('product_template_id')
    def _compute_show_configure_button(self):
        for line in self:
            line.show_configure_button = bool(line.product_template_id and line.product_template_id.is_pack)

    def action_open_combo_wizard(self):
        self.ensure_one()
        return {
            'name': _('Configure Combo'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line.combo.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
            }
        }



class SaleOrderLineComboWizard(models.TransientModel):
    _name = 'sale.order.line.combo.wizard'
    _description = 'Combo Product Wizard'

    order_line_id = fields.Many2one('sale.order.line', string='Order Line', required=True)
    required_pack_line_ids = fields.One2many('sale.order.line.combo.wizard.req.line', 'wizard_id', string='Required Products', readonly=True)
    optional_pack_line_ids = fields.One2many('sale.order.line.combo.wizard.opt.line', 'wizard_id', string='Optional Products')

    def action_confirm(self):
        order = self.order_line_id.order_id
        # Create lines for required
        for line in self.required_pack_line_ids:
            if line.product_id:
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                })
        # Create lines for optional
        for line in self.optional_pack_line_ids:
            if line.product_id:
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                })
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderLineComboWizard, self).default_get(fields_list)
        order_line_id = self.env.context.get('default_order_line_id')
        if order_line_id:
            line = self.env['sale.order.line'].browse(order_line_id)
            packs = line.product_id.product_tmpl_id.pack_ids
            req_lines = []
            opt_lines = []
            for p in packs:
                # If pack.product_ids has multiple products we leave selection to user for optional;
                if p.is_required:
                    # Choose first product if multiple exist
                    prod = p.product_ids and p.product_ids[0] or False
                    if prod:
                        req_lines.append((0, 0, {'product_id': prod.id, 'qty': 1.0}))
                else:
                    # For optional, add an empty line so user can choose
                    opt_lines.append((0, 0, {'qty': 1.0}))
            if req_lines:
                res['required_pack_line_ids'] = req_lines
            if opt_lines:
                res['optional_pack_line_ids'] = opt_lines
        return res


class SaleOrderLineComboWizardReqLine(models.TransientModel):
    _name = 'sale.order.line.combo.wizard.req.line'
    _description = 'Combo Wizard Required Line'

    wizard_id = fields.Many2one('sale.order.line.combo.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
    qty = fields.Float(string='Quantity', default=1.0)


class SaleOrderLineComboWizardOptLine(models.TransientModel):
    _name = 'sale.order.line.combo.wizard.opt.line'
    _description = 'Combo Wizard Optional Line'

    wizard_id = fields.Many2one('sale.order.line.combo.wizard', string='Wizard')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Quantity', default=1.0)