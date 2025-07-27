# -*- coding: utf-8 -*-

from uuid import uuid4
from odoo import api, fields, models, _
from odoo import exceptions
from datetime import datetime, timedelta, date

class ResPartner(models.Model):

    _inherit = 'res.partner'

    custom_state = fields.Char(string="State")
    is_member_pos = fields.Boolean(string="Member",default=False)
    
    def get_membership_code(self):
        card = self.env['membership.card'].sudo().search(
            [('customer_id', '=', self.id), ('expiry_date', '>=', date.today().strftime("%Y-%m-%d"))], limit=1)
        if card and card.state == 'confirm':
            return card.code
        elif card and (card.state == 'cancel' or card.state == 'draft'):
            return "Your card is not activated!"
        else:
            return f"Card Doesn't Exist for {self.name}"

    def get_total_sale_previous_year(self):
        card = self.env['membership.card'].sudo().search(
            [('customer_id', '=', self.id)])
        if card:
            from_date = (card.issue_date-timedelta(days=365)
                         ).strftime("%Y-%m-%d")
            to_date = card.issue_date.strftime("%Y-%m-%d")
            orders = self.env['pos.order'].sudo().search(
                [('state', '=', 'paid'), ('partner_id', '=', self.id), ('date_order', '>=', from_date), ('date_order', '<=', to_date)])

            return sum(orders.mapped('amount_total'))
        return 0

    def get_total_sale_current_year(self):
        card = self.env['membership.card'].sudo().search(
            [('customer_id', '=', self.id)])
        if card:
            from_date = card.issue_date.strftime("%Y-%m-%d")
            to_date = card.expiry_date.strftime("%Y-%m-%d")
            orders = self.env['pos.order'].sudo().search(
                [('state', 'in', ['paid','done']), ('partner_id', '=', self.id), ('date_order', '>=', from_date), ('date_order', '<=', to_date)])

            return sum(orders.mapped('amount_total'))
        return 0

    def get_total_yearly_sale_from_now(self):
        card = self.env['membership.card'].sudo().search(
            [('customer_id', '=', self.id)])
        if card:
            from_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")
            to_date = date.today().strftime("%Y-%m-%d")
            orders = self.env['pos.order'].sudo().search(
                [('state', 'in', ['paid','done']), ('partner_id', '=', self.id), ('date_order', '>=', from_date), ('date_order', '<=', to_date)])

            return sum(orders.mapped('amount_total'))
        return 0

class PosOrderLine(models.Model):

    _inherit = 'pos.order.line'
    association_id = fields.Many2one("gift.association", string="Product Or Gift")
    
    def _export_for_ui(self, orderline):
        result = super()._export_for_ui(orderline)

        result['association_id'] = orderline.association_id
        return result

    def _order_line_fields(self, line, session_id=None):
        result = super()._order_line_fields(line, session_id)
        print(result)
        
        return result
    

class PosOrder(models.Model):

    _inherit = 'pos.order'

    membership_card_id = fields.Many2one(
        "membership.card", string="membership card")
    membership_code = fields.Char(
        string='Membership Code', related='membership_card_id.code', store=True)

    def _order_fields(self, ui_order):
        """ Prepare dictionary for create method """
        result = super()._order_fields(ui_order)
        result['membership_card_id'] = ui_order.get('membership_card_id')
        return result
    
    

    @api.model
    def write(self, vals):

        order = super(PosOrder, self).write(vals)
        for odr in self:
            if odr.state == 'paid':
                order_meta = self.env['membership.card.metadata'].sudo().search(
                    [('order_ref', '=', odr.name)])
                if not order_meta:
                    free_products = odr.lines.filtered(
                        lambda lm: lm.price_unit == 0 and lm.product_id.default_code != 'DISC')
                    gifts = [(0, 0, {'product_id': gift.product_id.id,
                              'qty': gift.qty,'association_id':gift.association_id.id}) for gift in free_products]
                    metadata_obj = self.env['membership.card.metadata'].sudo().create(
                        {'card_id': odr.membership_card_id.id, 'is_discount_used': True, 'gift_ids': gifts, 'order_ref': odr.name})
                    
                    # for reducing the association applied times
                    uniq_associ = {}
                    for gift in free_products:
                        if gift.association_id.id in uniq_associ:
                            pass
                        else:
                            uniq_associ[gift.association_id.id] = True
                            association_applied_ids = odr.membership_card_id.membership_association_applied_times.filtered(lambda lm: lm.association_id.id == gift.association_id.id)
                            for acc_applied_obj in association_applied_ids:
                                acc_applied_obj.applied_times -= 1

                        
        return order


class GiftInfo(models.Model):

    _name = 'gift.info'

    product_id = fields.Many2one("product.product", string="Product Or Gift", domain="[('available_in_pos','=',True)]")
    qty = fields.Integer(string='Qty')

   
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, f"{rec.product_id.name}-qty({rec.qty})"))

        return result

class GiftAssociation(models.Model):
    _name = 'gift.association'
    _rec_name = 'name'
    name = fields.Char(string='Description',compute='_compute_description')
    gift_ids = fields.Many2many("gift.info", string="Product & Gifts")
    applied_times = fields.Integer(string="Applied Times", default=1)
    
    @api.depends('gift_ids')
    def _compute_description(self):
         for rec in self:
            if rec.gift_ids:
                names = rec.gift_ids[0].product_id.mapped('name')+ [" ..."]
                rec.name = ' or '.join(names)



class MembershipBenifits(models.Model):

    _name = 'membership.benifits'

    discount = fields.Float(string='Discount(%)',help='Discount percentage amount')
    gift_association_ids = fields.Many2many("gift.association", string="Product & Gifts")
    is_discount_applied_on_event_month_only = fields.Boolean(string="Discount in Event Month Only", default=False)
    

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.discount,
                          ','.join(rec.gift_association_ids.mapped('name')))))

        return result


class MembershipTypes(models.Model):
    """Creates membership types"""
    _name = 'membership.type'
    _inherit = 'mail.thread'
    _description = 'Customer Membership'

    name = fields.Char(string='Name', required=True, help='Name')
    default_period = fields.Float(default=1, readonly="True",
                                  string='Default Validity Period(Year)',
                                  help='Default validity period in year')
    membership_benifit_id = fields.Many2one('membership.benifits', string='Benifits',required=True)
    purchase_amount = fields.Float(string='Purchase Amount')
    level_sequence = fields.Integer(string='Level Sequence')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The membership name must be unique !'),
        ('level_sequence_uniq', 'unique (level_sequence)',
         'The sequenc must be unique its seems this is already exist!')
    ]

    def get_limit_membership(self, data):
        return self.env['membership.type'].sudo().browse(int(data['membership'])).purchase_amount

    def get_memebership_types(self, ip):
        return self.env['membership.type'].sudo().search([]).read()

    def get_products_gifts(self):
        lst = []
        for association in self.membership_benifit_id.gift_association_ids:
            for gift in association.gift_ids:
                lst.append({'product_id': gift.product_id.id, 'qty': gift.qty, 'name': gift.product_id.name,'association_id':association.id,'association_obj':association})

       
        return lst


class giftMetaData(models.Model):
    _name = 'gift.metadata'
    
    product_id = fields.Many2one("product.product", string="Product Or Gift")
    qty = fields.Integer(string='Qty')
    association_id = fields.Many2one("gift.association", string="Product Or Gift")

class MembershipCardMetaData(models.Model):
    _name = 'membership.card.metadata'

    card_id = fields.Many2one('membership.card', string='Membership Card')
    is_discount_used = fields.Boolean()
    gift_ids = fields.Many2many("gift.metadata", string="Product & Gifts")
    order_ref = fields.Char(string="ref")

class MembershipAssociationAppliedTimes(models.Model):
    _name = 'membership.association.applied.times'
    _description = 'Membership Association Applied Times'
    association_id = fields.Many2one("gift.association", string="Association")
    applied_times = fields.Integer(string="Applied Times", default=1)
    card_id = fields.Many2one("membership.card", string="Card")
    @api.onchange('card_id')
    def _onchange_card_id(self):

       
        if self.card_id:

            return {'domain': {'association_id': [('id', 'in', self.card_id.membership_id.membership_benifit_id.gift_association_ids.ids)]}}
        return {'domain': {'association_id': []}}

   
     
    

class MembershipCard(models.Model):
    """Creating membership card for the customers"""
    _name = 'membership.card'
    _inherit = 'mail.thread'
    _description = 'Membership Card'
    _rec_name = 'membership_id'

    membership_id = fields.Many2one('membership.type', string='Membership',
                                    required=True, help='Membership id')
    customer_id = fields.Many2one('res.partner', string="Customer",
                                  help='The customer')
    issue_date = fields.Date(string="Issue Date", help='Issue date',
                             default=fields.Date.today())
    validity = fields.Float(string='Validity(days)',
                            compute='_compute_validity',
                            help='Validity of membership card')
    expiry_date = fields.Date(string="Exp Date", default=fields.Date.today(),
                              help='Expiry date of membership card')
    special_date = fields.Date(string="Special Date")
    special_date_type = fields.Selection(
        selection=[
            ('birthday', 'BirthDay'),
            ('anvc', 'Anniversary'),
            ('other', 'Other'),

        ],
        default='birthday'
    )
    other_special_date_type = fields.Char(string="Other Special Date Type")
    code = fields.Char(string="Code", help='Unique code for the card',
                       readonly=True)
    membership_code_button = fields.Boolean(default=False, string="Visibility",
                                            help='The code generation button visibility')
    discount = fields.Float(
        string='Discount(%)', help='Discount percentage amount', compute='_compute_discount')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')],
        default='draft', string='State', help='State of the membership')
    sale_count = fields.Integer(compute='compute_count')
    total_sale_count = fields.Integer(compute='compute_total_count')
    membership_association_applied_times = fields.One2many('membership.association.applied.times', 'card_id', string="Applied Times")

    @api.model
    def create(self, vals):
       

        record = super(MembershipCard, self).create(vals)
        for rec in record:
            if rec.customer_id:
                rec.customer_id.is_member_pos = True


        return record
    @api.onchange('membership_id')
    def _onchange_membership_id(self):
        """ Reset and recreate One2many records when membership_id changes """
        if self.membership_id:
            # Clear existing One2many records
            self.membership_association_applied_times = [(5, 0, 0)]

            # Create new records
            new_records = []
            for obj in self.membership_id.membership_benifit_id.gift_association_ids:
                new_records.append((0, 0, {'association_id': obj.id, 'applied_times': obj.applied_times, 'card_id': self.id})) 
            
            self.membership_association_applied_times = new_records
    
    def get_meta_data(self): 
        gifts_info = dict()
        discount_used = False
        order_meta = self.env['membership.card.metadata'].sudo().search(
            [('card_id', '=', self.id)])
        order_meta = order_meta.filtered(lambda lm: lm.create_date.date(
        ) >= self.issue_date and lm.create_date.date() <= self.expiry_date)
        for obj in order_meta.mapped('gift_ids'):
            discount_used = True
            if obj.product_id.id in gifts_info:
                if obj.association_id.id in gifts_info[obj.product_id.id]:
                    gifts_info[obj.product_id.id][obj.association_id.id] += obj.qty
                else:
                    gifts_info[obj.product_id.id].update({obj.association_id.id:obj.qty})
            else:
                gifts_info[obj.product_id.id] = {obj.association_id.id:obj.qty}
        
        return gifts_info, discount_used

    
    def check_validity(self):
        memberships = self.env['membership.type'].sudo().search([])
        for rec in self.env['membership.card'].sudo().search([]):
            print('ander ayya')
            current_year_sale = rec.customer_id.get_total_yearly_sale_from_now()
            print(current_year_sale)
            matched = False
            if current_year_sale < rec.membership_id.purchase_amount:
                # Copy the original memberships list
                memberships_filtered = memberships.filtered(
                    lambda lm: lm.level_sequence < rec.membership_id.level_sequence)
                for membership in memberships_filtered:
                    if current_year_sale >= membership.purchase_amount:
                        rec.membership_id = membership.id
                        rec.issue_date = date.today()
                        rec.expiry_date = date.today() + timedelta(days=365)
                        rec.state = 'confirm'
                        matched = True
                        
                if not matched:
                    rec.state = 'cancel'
        
            else:
                # Copy the original memberships list
                memberships_filtered = memberships.filtered(
                    lambda lm: lm.level_sequence > rec.membership_id.level_sequence)
                for membership in memberships_filtered:
                    if current_year_sale >= membership.purchase_amount:
                        rec.membership_id = membership.id
                        rec.issue_date = date.today()
                        rec.expiry_date = date.today() + timedelta(days=365)
                        rec.state = 'confirm'
                        break




    def compute_count(self):
        for record in self:
            record.sale_count = self.env['pos.order'].sudo().search_count(
                [('state', '=', 'paid'), ('membership_card_id', '=', self.id)])

    def compute_total_count(self):
        for record in self:
            record.total_sale_count = self.env['pos.order'].sudo().search_count(
                [('state', '=', 'paid'), ('partner_id', '=', self.customer_id.id)])

    def action_view_sales(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'domain': [('membership_card_id', '=', self.id)],
            'context': "{'create': False}"
        }
    def action_view_total_sales(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'domain': [('partner_id', '=', self.customer_id.id)],
            'context': "{'create': False}"
        }

    @api.depends('membership_id.membership_benifit_id', 'membership_id.membership_benifit_id.discount')
    def _compute_discount(self):
        for rec in self:
            rec.discount = rec.membership_id.membership_benifit_id.discount

    @api.onchange('expiry_date')
    def _onchange_expiry_date(self):
        """This is used to check the expiry date of the membership"""
        if self.expiry_date < fields.Date.today():
            raise exceptions.ValidationError(_(
                "Please select a Valid Date."
            ))

    def generate_code(self):
        """Used to generate the code for membership card"""
        self.code = 'COUPON' + str(uuid4())[7:-18]
        self.membership_code_button = True

    def action_membership_confirm(self):
        """Used to confirm the membership"""
        self.state = 'confirm'

    def action_membership_reset_draft(self):
        """Used to reset to draft the membership"""
        self.state = 'draft'

    def action_membership_canceled(self):
        """Cancels the membership"""
        self.state = 'cancel'

    def _compute_validity(self):
        """Computes the validity"""
        fmt = '%Y-%m-%d'
        date_from = datetime.strptime(str(self.issue_date), fmt)
        date_to = datetime.strptime(str(self.expiry_date), fmt)
        duration = str((date_to - date_from).days)
        self.validity = duration

    def membership_card_check(self, customer_input):
        """Checks the validity of the membership card"""
        card = self.env['membership.card'].sudo().search(
            [('customer_id.id', '=', customer_input[0]['customer']),
             ('code', '=', customer_input[0]['customerInput']),
             ('expiry_date', '>', fields.Date.today()),
             ('state', '=', 'confirm')])
        if card:
            membership_discount = card.mapped(
                'discount')
            membership_product = int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'pos_membership_product_id'))

            applicable_gifts = card.membership_id.get_products_gifts()
            metadata_gifts, discount_used = card.get_meta_data()
            
            for product_id, assoc_obj in metadata_gifts.items():
                for assoc_id,qty in assoc_obj.items():
                    for appl_gift in applicable_gifts:
                        if appl_gift['product_id'] == product_id and appl_gift['association_id'] == assoc_id:
                            appl_gift['qty'] -= qty

                        if appl_gift['association_id'] == assoc_id and appl_gift['product_id'] != product_id:
                            appl_gift['qty'] = 0 # putting qty 0 so that other products should remove by following or condition

            
            applicable_gifts = list(
                filter(lambda d: d['qty'] > 0, applicable_gifts))

            # bipul new req applied times
            for gift in applicable_gifts:
                ass_obj = card.membership_association_applied_times.filtered(lambda lm: lm.association_id.id == gift['association_obj'].id )
                if card.membership_association_applied_times:
                    if ass_obj.applied_times == 1:
                        pass
                    else:
                        gift['qty'] = 1
                    


           
            
            res = {
                'customer_name': card.customer_id.name,
                'membership': card.membership_id.name,
                'discount': 0 if discount_used else membership_discount[0],
                'product_id': membership_product,
                'gifts': applicable_gifts,
                'card_id': card.id,
                'purchase_amount': card.customer_id.get_total_sale_current_year(),
                'membership_limit_amount': card.membership_id.purchase_amount,
                'state': card.state,
                'is_discount_applied': card.find_event_month_if_applied()
            }
            print(res)
            return res
        else:
            return 0

    def find_event_month_if_applied(self):
        if self.membership_id.membership_benifit_id.is_discount_applied_on_event_month_only:
            if self.special_date.month == date.today().month and self.special_date.year == date.today().year:
                return True
            else:
                return False
        return True
    def apply_card(self, data):
        pass

    def create_upgrade_membership(self, data):
        card = self.env['membership.card'].sudo().search(
            [('customer_id.id', '=', data['customer']),
             ('state', '=', 'confirm')])
        if card:
            card.write({
                'membership_id': int(data['membership']),
                'expiry_date': datetime.today() + timedelta(days=365),
                'special_date': data['special_date'] if data['special_date'] else False ,
                'special_date_type': data['special_day'],
                'other_special_date_type': data['other_type']

            })

        else:
            card = self.env['membership.card'].sudo().create({
                'membership_id': int(data['membership']),
                'expiry_date': datetime.today() + timedelta(days=365),
                'state': 'confirm',
                'customer_id': int(data['customer']),
                'special_date': data['special_date'] if data['special_date'] else False,
                'special_date_type': data['special_day'],
                'other_special_date_type': data['other_type']
            })
            card.generate_code()
        return card.read()


class POSConfig(models.Model):
    _inherit = "pos.config"

    visible_membership_btn = fields.Boolean("Membership ?")


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_partner(self):
        res = super(PosSession, self)._loader_params_res_partner()
        add_list = ["custom_state"]
        res['search_params']['fields'].extend(add_list)
        return res

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        loaded_data['visible_membership_btn'] = self.config_id.visible_membership_btn

    @api.model
    def _pos_ui_models_to_load(self):
        """This is used to load a new model to pos session"""
        result = super()._pos_ui_models_to_load()
        result += [
            'res.config.settings',
        ]
        return result

    def _loader_params_res_config_settings(self):
        """This is used to load the model fields"""
        return {
            'search_params': {
                'fields': ['visible_membership_btn'],
            }
        }

    def _get_pos_ui_res_config_settings(self, params):
        """This is used to load the model"""
        return self.env['res.config.settings'].sudo().search_read(
            **params['search_params'])


class ResConfigSettings(models.TransientModel):
    """This class used to add fields in the settings model"""
    _inherit = 'res.config.settings'

    pos_membership_product_id = fields.Many2one('product.product',
                                                string="Membership Product",
                                                help="Membership product",
                                                compute='_compute_pos_membership_discount_product_id',
                                                store=True, readonly=False)
    visible_membership_btn = fields.Boolean(string="Pos Membership",
                                            help="Pos module's pos membership")

    @api.depends('visible_membership_btn')
    def _compute_pos_membership_discount_product_id(self):
        """This is used to compute the default discount product of membership"""
        for rec in self:
            
            self.env['ir.config_parameter'].sudo().set_param('stock.group_product_variant',True)
            discount_prod = self.env['product.product'].sudo().search([('default_code', '=', 'DISC')], limit=1)
            if discount_prod:
                rec.pos_membership_product_id = discount_prod.id
            else:
                discount_prod = self.env['product.product'].sudo().create({
                    'name': 'Discount',
                    'default_code': 'DISC',
                    'detailed_type': 'service',
                    'sale_ok': True,
                    'available_in_pos':True
                })
                rec.pos_membership_product_id = discount_prod.id

            

    def get_values(self):
        """Getting the values from the transient model"""
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        visible_membership_btn = params.get_param('pos_membership_custom.'
                                                  'visible_membership_btn')
        res.update(
            pos_membership_product_id=int(
                self.env['ir.config_parameter'].sudo().get_param(
                    'pos_membership_product_id')),
            visible_membership_btn=visible_membership_btn
        )
        return res

    @api.model
    def set_values(self):
        """ Set values for the fields """
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'pos_membership_product_id',
            self.pos_membership_product_id.id)
        self.env['ir.config_parameter'].sudo().set_param(
            'pos_membership_custom.visible_membership_btn',
            self.visible_membership_btn)
        if self.pos_membership_product_id:
            if not (self.pos_membership_product_id.available_in_pos):
                raise exceptions.UserError(
                    "The discount product seems misconfigured.Make sure it is "
                    "flagged as 'Can be Sold' and 'Available in Point of Sale")
