from odoo import models, fields

# class ProductPack(models.Model):
#     _name = 'product.pack'
#     _description = 'Product Pack'

#     bi_product_template = fields.Many2one(comodel_name='product.template', string='Product pack')
#     bi_product_product = fields.Many2one(comodel_name='product.product', string='Product pack.',
#                                          related='bi_product_template.product_variant_id')
#     name = fields.Char(related='category_id.name', readonly=True)
#     is_required = fields.Boolean('Required')
#     category_id = fields.Many2one('pos.category', 'Category', required=True)
#     product_ids = fields.Many2many(comodel_name='product.product', string='Product', required=True,
#                                    domain="[('pos_categ_id','=', category_id)]")