# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesStock(http.Controller):
#     @http.route('/staples_stock/staples_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_stock/staples_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_stock.listing', {
#             'root': '/staples_stock/staples_stock',
#             'objects': http.request.env['staples_stock.staples_stock'].search([]),
#         })

#     @http.route('/staples_stock/staples_stock/objects/<model("staples_stock.staples_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_stock.object', {
#             'object': obj
#         })
