# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesSale(http.Controller):
#     @http.route('/staples_sale/staples_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_sale/staples_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_sale.listing', {
#             'root': '/staples_sale/staples_sale',
#             'objects': http.request.env['staples_sale.staples_sale'].search([]),
#         })

#     @http.route('/staples_sale/staples_sale/objects/<model("staples_sale.staples_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_sale.object', {
#             'object': obj
#         })
