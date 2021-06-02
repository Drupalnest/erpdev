# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesPurchase(http.Controller):
#     @http.route('/staples_purchase/staples_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_purchase/staples_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_purchase.listing', {
#             'root': '/staples_purchase/staples_purchase',
#             'objects': http.request.env['staples_purchase.staples_purchase'].search([]),
#         })

#     @http.route('/staples_purchase/staples_purchase/objects/<model("staples_purchase.staples_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_purchase.object', {
#             'object': obj
#         })
