# -*- coding: utf-8 -*-
# from odoo import http


# class PosMembershipCustom(http.Controller):
#     @http.route('/pos_membership_custom/pos_membership_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_membership_custom/pos_membership_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_membership_custom.listing', {
#             'root': '/pos_membership_custom/pos_membership_custom',
#             'objects': http.request.env['pos_membership_custom.pos_membership_custom'].search([]),
#         })

#     @http.route('/pos_membership_custom/pos_membership_custom/objects/<model("pos_membership_custom.pos_membership_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_membership_custom.object', {
#             'object': obj
#         })
